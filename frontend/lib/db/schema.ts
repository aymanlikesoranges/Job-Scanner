import { integer, pgTable, timestamp, varchar } from "drizzle-orm/pg-core";

export const emails = pgTable("emails", {
    id: integer().primaryKey().generatedAlwaysAsIdentity(),
    email: varchar({ length: 255 }).notNull().unique(),
    createdAt: timestamp().defaultNow()
});