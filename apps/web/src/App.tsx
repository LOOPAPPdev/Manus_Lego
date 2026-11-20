import { useEffect, useState } from 'react';
import { CatalogPage } from './pages/CatalogPage.js';
import { TemplatePage } from './pages/TemplatePage.js';
import { GovernancePage } from './pages/GovernancePage.js';
import { AboutPage } from './pages/AboutPage.js';

export type Route =
  | { name: 'catalog' }
  | { name: 'template'; id: string }
  | { name: 'governance' }
  | { name: 'about' };

export function parseRoute(hash: string): Route {
  const clean = hash.replace(/^#\/?/, '');
  const [segment, ...rest] = clean.split('/');
  if (segment === 'template' && rest.length > 0) {
    return { name: 'template', id: decodeURIComponent(rest.join('/')) };
  }
  if (segment === 'governance') {
    return { name: 'governance' };
  }
  if (segment === 'about') {
    return { name: 'about' };
  }
  return { name: 'catalog' };
}

function useRoute(): Route {
  const [route, setRoute] = useState<Route>(() => parseRoute(window.location.hash));
  useEffect(() => {
    const onChange = (): void => setRoute(parseRoute(window.location.hash));
    window.addEventListener('hashchange', onChange);
    return () => window.removeEventListener('hashchange', onChange);
  }, []);
  return route;
}

const NAV: Array<{ href: string; label: string; match: Route['name'] }> = [
  { href: '#/', label: 'Catalog', match: 'catalog' },
  { href: '#/governance', label: 'Gates & traceability', match: 'governance' },
  { href: '#/about', label: 'About', match: 'about' },
];

export function App() {
  const route = useRoute();

  return (
    <div className="app">
      <a className="skip-link" href="#main">
        Skip to content
      </a>
      <header className="header">
        <div className="header__inner">
          <a className="brand" href="#/">
            <span className="brand__mark" aria-hidden="true">
              ◧
            </span>
            <span>
              <strong>Manus LEGO</strong>
              <small>Reference catalog</small>
            </span>
          </a>
          <nav className="nav" aria-label="Primary">
            {NAV.map((item) => (
              <a
                key={item.href}
                href={item.href}
                className={route.name === item.match || (item.match === 'catalog' && route.name === 'template') ? 'nav__link nav__link--active' : 'nav__link'}
                aria-current={route.name === item.match ? 'page' : undefined}
              >
                {item.label}
              </a>
            ))}
          </nav>
        </div>
      </header>

      <main id="main" className="main">
        {route.name === 'catalog' ? <CatalogPage /> : null}
        {route.name === 'template' ? <TemplatePage id={route.id} /> : null}
        {route.name === 'governance' ? <GovernancePage /> : null}
        {route.name === 'about' ? <AboutPage /> : null}
      </main>

      <footer className="footer">
        <div className="footer__inner">
          <p>
            Read-only explorer. The catalog records <em>references</em> to third-party templates; it does not vendor their code and
            does not claim runtime verification.
          </p>
          <p className="muted small">
            NIST SP 800-218 / 800-204D / 800-218A / AI RMF / 800-190 inform the controls. Passing gates are implementation
            evidence, not certification.
          </p>
        </div>
      </footer>
    </div>
  );
}
