/**
 * Minimal structured logger emitting one JSON object per line.
 *
 * Security intent: secrets must never reach logs. Values are redacted before
 * serialisation, and the logger deliberately has no free-form string
 * interpolation of untrusted catalog text into the message field.
 */

export type LogLevel = 'debug' | 'info' | 'warn' | 'error';

const LEVEL_ORDER: Record<LogLevel, number> = { debug: 10, info: 20, warn: 30, error: 40 };
const REDACTED_KEYS = /(token|secret|password|authorization|api[-_]?key|cookie)/i;
const REDACTED = '[redacted]';

export interface LogFields {
  [key: string]: unknown;
}

export interface Logger {
  debug(message: string, fields?: LogFields): void;
  info(message: string, fields?: LogFields): void;
  warn(message: string, fields?: LogFields): void;
  error(message: string, fields?: LogFields): void;
  child(bindings: LogFields): Logger;
}

export function redact(value: unknown, depth = 0): unknown {
  if (depth > 6) {
    return '[truncated]';
  }
  if (Array.isArray(value)) {
    return value.slice(0, 50).map((item) => redact(item, depth + 1));
  }
  if (value && typeof value === 'object') {
    const out: Record<string, unknown> = {};
    for (const [key, item] of Object.entries(value as Record<string, unknown>)) {
      out[key] = REDACTED_KEYS.test(key) ? REDACTED : redact(item, depth + 1);
    }
    return out;
  }
  if (typeof value === 'string' && value.length > 2000) {
    return `${value.slice(0, 2000)}…`;
  }
  return value;
}

export function createLogger(options: {
  level?: LogLevel;
  service: string;
  bindings?: LogFields;
  sink?: (line: string) => void;
}): Logger {
  const threshold = LEVEL_ORDER[options.level ?? 'info'];
  const sink = options.sink ?? ((line: string) => process.stdout.write(`${line}\n`));
  const base = { service: options.service, ...options.bindings };

  const emit = (level: LogLevel, message: string, fields?: LogFields): void => {
    if (LEVEL_ORDER[level] < threshold) {
      return;
    }
    sink(
      JSON.stringify(
        redact({
          ts: new Date().toISOString(),
          level,
          message,
          ...base,
          ...fields,
        }),
      ),
    );
  };

  return {
    debug: (message, fields) => emit('debug', message, fields),
    info: (message, fields) => emit('info', message, fields),
    warn: (message, fields) => emit('warn', message, fields),
    error: (message, fields) => emit('error', message, fields),
    child: (bindings) =>
      createLogger({ level: options.level, service: options.service, bindings: { ...base, ...bindings }, sink }),
  };
}
