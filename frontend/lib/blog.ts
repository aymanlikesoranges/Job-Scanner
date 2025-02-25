import { join } from "path";
import fs from "fs";
import { Metadata } from "next";

const postsDirectory = join(process.cwd(), "_blog");

export function getAllPostSlugs() {
  const filenames: string[] = fs.readdirSync(postsDirectory);
  const slugs = [];

  for (const filename of filenames) {
    slugs.push({ slug: filename.replace(/\.mdx$/, "") });
  }

  console.log(slugs);
  return slugs;
}

interface PostInfo {
  slug: string;
  metadata: Metadata;
}

export async function getAllPosts(): Promise<Array<PostInfo>> {
  const filenames: string[] = fs.readdirSync(postsDirectory);
  const posts: PostInfo[] = [];
  for (const filename of filenames) {
    const slug = filename.replace(/\.mdx$/, "");
    const { default: Post, metadata } = await getPost(slug);
    posts.push({ slug: slug, metadata: metadata });
  }
  return posts;
}

export async function getPost(
  slug: string
): Promise<{ default: any; metadata: Metadata }> {
  const post = await import(`@/_blog/${slug}.mdx`);
  return post;
}

export async function generateStaticParams() {
  return getAllPostSlugs();
}

export const dynamicParams = false;
