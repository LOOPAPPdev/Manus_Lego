/**
 * Fixed-window in-memory limiter.
 *
 * Intent: a public read-only API must not be usable as an amplification vector
 * or a catalog-scraping engine. This is a per-instance control; a multi-instance
 * deployment should move the counter to a shared store (see
 * docs/decisions/0006-api-read-only-design.md).
 */
export interface RateLimitDecision {
  allowed: boolean;
  remaining: number;
  resetSeconds: number;
}

export class FixedWindowLimiter {
  private readonly limit: number;
  private readonly windowMs: number;
  private readonly buckets = new Map<string, { count: number; resetAt: number }>();
  private readonly maxKeys: number;

  constructor(limitPerWindow: number, windowMs = 60_000, maxKeys = 10_000) {
    this.limit = limitPerWindow;
    this.windowMs = windowMs;
    this.maxKeys = maxKeys;
  }

  check(key: string, now = Date.now()): RateLimitDecision {
    const existing = this.buckets.get(key);
    if (!existing || existing.resetAt <= now) {
      if (this.buckets.size >= this.maxKeys) {
        this.evict(now);
      }
      this.buckets.set(key, { count: 1, resetAt: now + this.windowMs });
      return { allowed: true, remaining: this.limit - 1, resetSeconds: Math.ceil(this.windowMs / 1000) };
    }

    existing.count += 1;
    const resetSeconds = Math.max(1, Math.ceil((existing.resetAt - now) / 1000));
    return {
      allowed: existing.count <= this.limit,
      remaining: Math.max(0, this.limit - existing.count),
      resetSeconds,
    };
  }

  private evict(now: number): void {
    for (const [key, bucket] of this.buckets) {
      if (bucket.resetAt <= now) {
        this.buckets.delete(key);
      }
    }
    // Still full of live buckets: drop the oldest insertions to bound memory.
    while (this.buckets.size >= this.maxKeys) {
      const oldest = this.buckets.keys().next().value;
      if (oldest === undefined) {
        break;
      }
      this.buckets.delete(oldest);
    }
  }
}
