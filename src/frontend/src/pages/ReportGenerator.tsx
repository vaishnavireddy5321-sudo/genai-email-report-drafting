/**
 * Report Generator page component
 */

import { useState, useEffect } from 'react';
import { useAppDispatch, useAppSelector } from '../store/hooks';
import { generateDocument, clearError, clearCurrentDocument } from '../store/documentsSlice';

const TONE_OPTIONS = ['professional', 'formal', 'casual', 'friendly'];

export default function ReportGenerator() {
  const [tone, setTone] = useState('formal');
  const [context, setContext] = useState('');
  const dispatch = useAppDispatch();
  const { loading, error, currentDocument } = useAppSelector((state) => state.documents);

  useEffect(() => {
    return () => {
      dispatch(clearError());
      dispatch(clearCurrentDocument());
    };
  }, [dispatch]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!context.trim()) return;

    dispatch(clearCurrentDocument());
    dispatch(
      generateDocument({
        doc_type: 'report',
        tone,
        input_context: context,
      })
    );
  };

  const handleClear = () => {
    setContext('');
    dispatch(clearCurrentDocument());
    dispatch(clearError());
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-slate-900">Report Generator</h1>
        <p className="text-slate-600 mt-2">
          Generate professional reports with AI assistance
        </p>
      </div>

      {error && (
        <div 
          role="alert" 
          aria-live="assertive" 
          className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg"
        >
          {error}
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input Section */}
        <div className="bg-white rounded-xl shadow-md p-6">
          <h2 className="text-xl font-semibold text-slate-900 mb-4">Input</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="tone" className="block text-sm font-medium text-slate-700 mb-2">
                Tone
              </label>
              <select
                id="tone"
                value={tone}
                onChange={(e) => setTone(e.target.value)}
                aria-label="Select report tone"
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition"
              >
                {TONE_OPTIONS.map((option) => (
                  <option key={option} value={option}>
                    {option.charAt(0).toUpperCase() + option.slice(1)}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label htmlFor="context" className="block text-sm font-medium text-slate-700 mb-2">
                Context
              </label>
              <textarea
                id="context"
                value={context}
                onChange={(e) => setContext(e.target.value)}
                required
                aria-required="true"
                aria-label="Report context and requirements"
                rows={10}
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition resize-none"
                placeholder="Describe the report topic, key points, and any specific requirements..."
              />
            </div>

            <div className="flex gap-3">
              <button
                type="submit"
                disabled={loading || !context.trim()}
                aria-busy={loading}
                aria-label={loading ? 'Generating report, please wait' : 'Generate report from provided context'}
                className="flex-1 bg-slate-200 text-slate-700 py-2 rounded-lg font-medium border border-slate-300 hover:bg-slate-300 hover:border-slate-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-slate-400 disabled:opacity-50 disabled:cursor-not-allowed transition"
              >
                {loading ? 'Generating...' : 'Generate Report'}
              </button>
              <button
                type="button"
                onClick={handleClear}
                aria-label="Clear input and output"
                className="px-6 bg-slate-200 text-slate-700 py-2 rounded-lg font-medium border border-slate-300 hover:bg-slate-300 hover:border-slate-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-slate-400 disabled:opacity-50 disabled:cursor-not-allowed transition"
              >
                Clear
              </button>
            </div>
          </form>
        </div>

        {/* Output Section */}
        <div className="bg-white rounded-xl shadow-md p-6 flex flex-col">
          <h2 className="text-xl font-semibold text-slate-900 mb-4">Output</h2>
          <div aria-live="polite" aria-atomic="true" className="flex-1 overflow-y-auto pr-2 [&::-webkit-scrollbar]:w-1 [&::-webkit-scrollbar-track]:bg-slate-100 [&::-webkit-scrollbar-thumb]:bg-slate-300 [&::-webkit-scrollbar-thumb]:rounded-full [&::-webkit-scrollbar-thumb]:hover:bg-slate-400" style={{ maxHeight: '500px' }}>
          {loading ? (
            <div className="flex items-center justify-center h-64" role="status" aria-label="Generating report">
              <div className="text-center">
                <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-primary-500 border-t-transparent"></div>
                <p className="mt-4 text-slate-600">Generating your report...</p>
              </div>
            </div>
          ) : currentDocument ? (
            <div className="space-y-4">
              <div className="bg-slate-50 rounded-lg p-4">
                <div className="text-sm text-slate-500 mb-2">
                  Generated on {new Date(currentDocument.created_at).toLocaleString()}
                </div>
                <div className="whitespace-pre-wrap text-slate-900">
                  {currentDocument.content || ''}
                </div>
              </div>
              <button
                onClick={() => {
                  navigator.clipboard.writeText(currentDocument.content || '');
                }}
                aria-label="Copy generated report to clipboard"
                className="w-full bg-slate-200 text-slate-700 py-2 rounded-lg font-medium border border-slate-300 hover:bg-slate-300 hover:border-slate-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-slate-400 disabled:opacity-50 disabled:cursor-not-allowed transition"
              >
                Copy to Clipboard
              </button>
            </div>
          ) : (
            <div className="flex items-center justify-center h-64 text-slate-400">
              <div className="text-center">
                <svg
                  className="mx-auto h-12 w-12 mb-4"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                  aria-hidden="true"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                  />
                </svg>
                <p>Your generated report will appear here</p>
              </div>
            </div>
          )}
          </div>
        </div>
      </div>
    </div>
  );
}
