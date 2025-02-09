import 'dotenv/config';
import { defineConfig } from 'drizzle-kit';
import fs from 'fs';

export default defineConfig({
    out: './drizzle',
    schema: './lib/db/schema.ts',
    dialect: 'postgresql',

    dbCredentials: {
        url: process.env.PG_CONNECTION_URL!,
    },
});