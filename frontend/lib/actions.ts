"use server";
import { db } from "@/lib/db/db";
import { emails } from "@/lib/db/schema";
import { redirect } from "next/navigation";
import { z } from "zod";

const schema = z.object({
  email: z.string().email("Invalid Email"),
});

export async function subscribeWaitlist(prevState: any, formData: FormData) {
  const validatedFields = schema.safeParse({
    email: formData.get("email"),
  });

  if (!validatedFields.success) {
    return { success: false, message: "Your email is incorrect" };
  }

  await db.insert(emails).values({ email: validatedFields.data.email }).onConflictDoNothing();

  return { success: true, message: "You've been added to the newsletter" };
}

