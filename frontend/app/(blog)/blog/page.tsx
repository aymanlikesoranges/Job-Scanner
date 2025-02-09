import { getAllPosts, getAllPostSlugs } from "@/lib/blog";
import Link from "next/link";

function Post({
  slug,
  title,
  description,
  date,
}: {
  slug: string;
  title: string;
  description: string;
  date: string;
}) {
  return (
    <li data-href="test" role="link" className="list-row">
      <Link className="w-full" href={`/blog/${slug}`}>
        <article>
          <h2 className="text-2xl font-bold">{title}</h2>
        </article>
        <p className="list-col-wrap text-xs mt-2">{description}</p>
        <h3 className="text-xs opacity-60 mt-4">{date}</h3>
      </Link>
    </li>
  );
}
<meta
  data-rh="true"
  property="article:published_time"
  content="2024-02-24T08:29:00.174Z"
></meta>;

export default async function Index() {
  const allPosts = await getAllPosts();

  return (
    <main>
      <div className="max-w-[500px] w-full mx-auto items-center">
        <Link className="link link-primary" href="/">
          Go back to landing page
        </Link>

        <h1 className="text-3xl font-bold mt-3">Recent Blog Posts</h1>

        <ul className="list bg-base-100 rounded-box shadow-md mt-5">
          {allPosts.map((post) => (
            <Post
              key={post.slug}
              slug={post.slug}
              title={post.metadata.title! as string}
              date={post.metadata.other!["createdAt"] as string}
              description={post.metadata.description!}
            ></Post>
          ))}
        </ul>
      </div>
    </main>
  );
}
