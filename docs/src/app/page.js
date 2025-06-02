import { allDocs } from 'contentlayer/generated'

export default function Home() {
  const doc = allDocs.find((doc) => doc.slugAsParams === '')

  return (
    <main className="relative py-6 lg:gap-10 lg:py-8 xl:grid xl:grid-cols-[1fr_300px]">
      <div className="mx-auto w-full min-w-0">
        <div className="mb-4">
          <h1 className="scroll-m-20 text-4xl font-bold tracking-tight">
            {doc.title}
          </h1>
          <p className="text-lg text-muted-foreground">{doc.description}</p>
        </div>
        <div className="prose max-w-none">
          <doc.body />
        </div>
      </div>
    </main>
  )
}
