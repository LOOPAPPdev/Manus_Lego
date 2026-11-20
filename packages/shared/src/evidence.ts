import { createHash } from 'node:crypto';
import { mkdirSync, readFileSync, renameSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';

/**
 * Evidence helpers.
 *
 * Every generated artifact carries a SHA-256 digest so a reviewer can prove the
 * report they read matches the bytes produced by a given commit. Writes are
 * atomic (temp file + rename) to avoid half-written evidence on interruption.
 */

export function sha256(content: string | Buffer): string {
  return createHash('sha256').update(content).digest('hex');
}

export function sha256File(path: string): string {
  return sha256(readFileSync(path));
}

export function stableStringify(value: unknown): string {
  const seen = new WeakSet<object>();
  const walk = (input: unknown): unknown => {
    if (Array.isArray(input)) {
      return input.map(walk);
    }
    if (input && typeof input === 'object') {
      if (seen.has(input)) {
        throw new Error('Cannot serialise a circular structure');
      }
      seen.add(input);
      const out: Record<string, unknown> = {};
      for (const key of Object.keys(input as Record<string, unknown>).sort()) {
        out[key] = walk((input as Record<string, unknown>)[key]);
      }
      return out;
    }
    return input;
  };
  return JSON.stringify(walk(value), null, 2);
}

export interface WrittenArtifact {
  path: string;
  sha256: string;
  bytes: number;
}

export function writeArtifact(path: string, content: string): WrittenArtifact {
  mkdirSync(dirname(path), { recursive: true });
  const payload = content.endsWith('\n') ? content : `${content}\n`;
  const temporary = join(dirname(path), `.${Date.now()}.tmp`);
  writeFileSync(temporary, payload, 'utf8');
  renameSync(temporary, path);
  return { path, sha256: sha256(payload), bytes: Buffer.byteLength(payload) };
}

export function writeJsonArtifact(path: string, value: unknown): WrittenArtifact {
  return writeArtifact(path, stableStringify(value));
}
