import type { ReactNode } from 'react';

export function Loading({ label = 'Loading' }: { label?: string }) {
  return (
    <div className="loading" role="status">
      <span className="spinner" aria-hidden="true" />
      <span>{label}…</span>
    </div>
  );
}

export function ErrorNotice({ message }: { message: string }) {
  return (
    <div className="notice notice--error" role="alert">
      <strong>Could not load data.</strong> {message}
    </div>
  );
}

export function Hint({ children }: { children: ReactNode }) {
  return <div className="notice notice--info">{children}</div>;
}
