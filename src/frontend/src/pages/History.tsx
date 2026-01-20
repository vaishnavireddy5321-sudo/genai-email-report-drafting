/**
 * History page component
 */

import { useEffect, useState } from 'react';
import { useAppDispatch, useAppSelector } from '../store/hooks';
import { fetchHistory } from '../store/documentsSlice';
import { documentsApi, ApiClientError } from '../api/client';

export default function History() {
  const [filterType, setFilterType] = useState<'all' | 'email' | 'report'>('all');
  const [expandedContent, setExpandedContent] = useState<Record<number, string>>({});
  const [loadingIds, setLoadingIds] = useState<Record<number, boolean>>({});
  const dispatch = useAppDispatch();
  const { items, loading, error } = useAppSelector((state) => state.documents);

  useEffect(() => {
    const params = filterType === 'all' ? {} : { doc_type: filterType };
    dispatch(fetchHistory(params));
  }, [dispatch, filterType]);

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const ensureFullContent = async (documentId: number) => {
    if (expandedContent[documentId] !== undefined || loadingIds[documentId]) {
      return;
    }

    setLoadingIds((prev) => ({ ...prev, [documentId]: true }));
    try {
      const detail = await documentsApi.getDetail(documentId);
      setExpandedContent((prev) => ({ ...prev, [documentId]: detail.document.content || '' }));
    } catch (err) {
      const message = err instanceof ApiClientError ? err.message : 'Failed to load document content';
      setExpandedContent((prev) => ({ ...prev, [documentId]: message }));
    } finally {
      setLoadingIds((prev) => ({ ...prev, [documentId]: false }));
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">History</h1>
          <p className="text-slate-600 mt-2">View your generated documents</p>
        </div>

        <div className="flex gap-2">
          <button
            onClick={() => setFilterType('all')}
            className={`px-4 py-2 rounded-lg font-medium border transition ${
              filterType === 'all'
                ? 'bg-primary-600 text-white border-primary-700'
                : 'bg-slate-200 text-slate-700 border-slate-300 hover:bg-slate-300 hover:border-slate-600'
            }`}
          >
            All
          </button>
          <button
            onClick={() => setFilterType('email')}
            className={`px-4 py-2 rounded-lg font-medium border transition ${
              filterType === 'email'
                ? 'bg-primary-600 text-white border-primary-700'
                : 'bg-slate-200 text-slate-700 border-slate-300 hover:bg-slate-300 hover:border-slate-600'
            }`}
          >
            Emails
          </button>
          <button
            onClick={() => setFilterType('report')}
            className={`px-4 py-2 rounded-lg font-medium border transition ${
              filterType === 'report'
                ? 'bg-primary-600 text-white border-primary-700'
                : 'bg-slate-200 text-slate-700 border-slate-300 hover:bg-slate-300 hover:border-slate-600'
            }`}
          >
            Reports
          </button>
        </div>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          {error}
        </div>
      )}

      {loading ? (
        <div className="flex items-center justify-center py-12">
          <div className="text-center">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-primary-500 border-t-transparent"></div>
            <p className="mt-4 text-slate-600">Loading history...</p>
          </div>
        </div>
      ) : items.length === 0 ? (
        <div className="bg-white rounded-xl shadow-md p-12 text-center">
          <svg
            className="mx-auto h-16 w-16 text-slate-400 mb-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
            />
          </svg>
          <h3 className="text-lg font-medium text-slate-900 mb-2">No documents yet</h3>
          <p className="text-slate-600">
            Generate your first email or report to see it here
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {items.map((doc) => (
            <div key={doc.id} className="bg-white rounded-xl shadow-md p-6">
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-3">
                  <span
                    className={`px-3 py-1 rounded-full text-xs font-medium ${
                      doc.doc_type === 'email'
                        ? 'bg-blue-100 text-blue-700'
                        : 'bg-purple-100 text-purple-700'
                    }`}
                  >
                    {doc.doc_type.charAt(0).toUpperCase() + doc.doc_type.slice(1)}
                  </span>
                  <span className="px-3 py-1 rounded-full text-xs font-medium bg-slate-100 text-slate-700">
                    {doc.tone}
                  </span>
                </div>
                <span className="text-sm text-slate-500">{formatDate(doc.created_at)}</span>
              </div>

              {doc.title && (
                <div className="mb-4">
                  <h3 className="text-sm font-medium text-slate-700 mb-2">Title:</h3>
                  <p className="text-sm text-slate-600 line-clamp-2">{doc.title}</p>
                </div>
              )}

              <div className="mb-4">
                <h3 className="text-sm font-medium text-slate-700 mb-2">Preview:</h3>
                <p className="text-sm text-slate-600 line-clamp-3">{doc.content_preview || '-'}</p>
              </div>

              <details
                className="group"
                onToggle={(e) => {
                  const el = e.currentTarget;
                  if (el.open) {
                    void ensureFullContent(doc.id);
                  }
                }}
              >
                <summary className="cursor-pointer text-primary-600 hover:text-primary-700 text-sm font-medium list-none flex items-center gap-2">
                  <span className="group-open:rotate-90 transition-transform">▶</span>
                  View generated content
                </summary>
                <div className="mt-4 bg-slate-50 rounded-lg p-4">
                  <div className="whitespace-pre-wrap text-sm text-slate-900">
                    {loadingIds[doc.id]
                      ? 'Loading...'
                      : (expandedContent[doc.id] ?? doc.content_preview ?? '')}
                  </div>
                  <button
                    onClick={() => {
                      const textToCopy = expandedContent[doc.id] ?? doc.content_preview ?? '';
                      navigator.clipboard.writeText(textToCopy);
                    }}
                    className="mt-3 px-4 py-2 bg-slate-200 text-slate-700 rounded-lg text-sm font-medium border border-slate-300 hover:bg-slate-300 hover:border-slate-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-slate-400 transition"
                  >
                    Copy to Clipboard
                  </button>
                </div>
              </details>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
