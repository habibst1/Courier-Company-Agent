import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

// Styles for markdown in assistant replies. `node` is pulled out so it isn't passed to the DOM.
// Inline code is styled on <code>; code blocks reset that style through <pre>.
const markdown = {
  p: ({ node, ...props }) => <p className="mb-2 last:mb-0" {...props} />,
  ul: ({ node, ...props }) => <ul className="mb-2 ml-2 list-inside list-disc" {...props} />,
  ol: ({ node, ...props }) => <ol className="mb-2 ml-2 list-inside list-decimal" {...props} />,
  li: ({ node, ...props }) => <li className="mb-1" {...props} />,
  strong: ({ node, ...props }) => <strong className="font-semibold" {...props} />,
  h1: ({ node, ...props }) => <h3 className="mb-2 mt-3 text-lg font-bold" {...props} />,
  h2: ({ node, ...props }) => <h3 className="mb-2 mt-3 font-semibold" {...props} />,
  h3: ({ node, ...props }) => <h4 className="mb-2 mt-2 font-semibold" {...props} />,
  a: ({ node, ...props }) => (
    <a className="text-primary-600 underline hover:text-primary-700" target="_blank" rel="noreferrer" {...props} />
  ),
  code: ({ node, ...props }) => (
    <code className="rounded bg-gray-200/70 px-1.5 py-0.5 font-mono text-[0.85em]" {...props} />
  ),
  pre: ({ node, ...props }) => (
    <pre
      className="my-2 overflow-x-auto rounded-lg bg-gray-100 p-3 text-sm [&>code]:bg-transparent [&>code]:p-0"
      {...props}
    />
  ),
  blockquote: ({ node, ...props }) => (
    <blockquote className="my-2 border-l-4 border-gray-300 pl-4 italic text-gray-600" {...props} />
  ),
  table: ({ node, ...props }) => (
    <div className="my-2 overflow-x-auto">
      <table className="min-w-full border-collapse border border-gray-300 text-sm" {...props} />
    </div>
  ),
  thead: ({ node, ...props }) => <thead className="bg-gray-100" {...props} />,
  tr: ({ node, ...props }) => <tr className="even:bg-gray-50" {...props} />,
  th: ({ node, ...props }) => (
    <th className="border border-gray-300 px-3 py-2 text-left font-semibold" {...props} />
  ),
  td: ({ node, ...props }) => <td className="border border-gray-300 px-3 py-2" {...props} />,
};

const bubbleStyles = {
  user: 'bg-primary-600 text-white rounded-br-none',
  assistant: 'border border-gray-200 bg-gray-50 text-gray-800 rounded-bl-none',
  error: 'border border-red-200 bg-red-50 text-red-800',
};

export default function MessageBubble({ message }) {
  const { role, content, streaming } = message;
  const isUser = role === 'user';
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`max-w-[85%] overflow-hidden rounded-2xl px-4 py-3 sm:max-w-md lg:max-w-xl ${
          bubbleStyles[role] ?? bubbleStyles.assistant
        }`}
      >
        {isUser || role === 'error' ? (
          <p className="whitespace-pre-wrap break-words">{content}</p>
        ) : (
          <div className="break-words">
            <ReactMarkdown remarkPlugins={[remarkGfm]} components={markdown}>
              {content}
            </ReactMarkdown>
            {streaming && (
              <span
                className="ml-0.5 inline-block h-4 w-1.5 animate-pulse bg-gray-400 align-middle"
                aria-hidden="true"
              />
            )}
          </div>
        )}
      </div>
    </div>
  );
}
