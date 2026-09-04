import fs from 'node:fs';
import postgres from 'postgres';

function loadEnv() {
  const path = new URL('../.env', import.meta.url);
  if (!fs.existsSync(path)) {
    console.error('Arquivo .env não encontrado em tracking/.env');
    process.exit(1);
  }
  for (const line of fs.readFileSync(path, 'utf8').replace(/\r/g, '').split('\n')) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const i = trimmed.indexOf('=');
    if (i < 0) continue;
    process.env[trimmed.slice(0, i).trim()] = trimmed.slice(i + 1).trim();
  }
}

loadEnv();

const url = process.env.DATABASE_URL;
if (!url) {
  console.error('DATABASE_URL não definida no .env');
  process.exit(1);
}

if (url.includes('[YOUR-PASSWORD]') || /:\[[^\]]+\]@/.test(url)) {
  console.error('Senha ainda com placeholder ou colchetes [ ]. Remova os colchetes.');
  process.exit(1);
}

const sql = postgres(url, { max: 1, connect_timeout: 15 });

try {
  const [events] = await sql`select count(*)::int as n from tracking_events`;
  const [persons] = await sql`select count(*)::int as n from persons`;
  console.log('OK — conectado ao Supabase');
  console.log('tracking_events:', events.n);
  console.log('persons:', persons.n);
} catch (error) {
  console.error('Falha na conexão:', error.message);
  console.error('');
  console.error('Checklist:');
  console.error('1. Supabase → Connect → Transaction pooler → copiar URI inteira');
  console.error('2. Substituir [YOUR-PASSWORD] pela senha (sem colchetes)');
  console.error('3. Se a senha tiver @ # % etc., precisa URL-encode');
  process.exit(1);
} finally {
  await sql.end();
}
