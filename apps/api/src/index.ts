import { buildServer } from './server.js';

const port = Number(process.env.LEGO_API_PORT ?? process.env.PORT ?? 8787);
const host = process.env.LEGO_API_HOST ?? '0.0.0.0';

const server = buildServer();

async function start(): Promise<void> {
  try {
    await server.listen({ port, host });
  } catch (error) {
    server.log.error(String(error));
    process.exitCode = 1;
  }
}

for (const signal of ['SIGINT', 'SIGTERM'] as const) {
  process.on(signal, () => {
    void server.close().then(() => {
      process.exit(0);
    });
  });
}

void start();
