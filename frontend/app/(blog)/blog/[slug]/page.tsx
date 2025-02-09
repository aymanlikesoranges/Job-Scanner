import { getAllPostSlugs, getPost } from "@/lib/blog";

export default async function Page({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const slug = (await params).slug;
  const { default: Post } = await getPost(slug);

  return <Post />;
}

export async function generateStaticParams() {
  const posts = getAllPostSlugs();
  return posts
}

export const dynamicParams = false;
