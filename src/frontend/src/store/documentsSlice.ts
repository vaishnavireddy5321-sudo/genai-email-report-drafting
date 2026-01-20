/**
 * Redux slice for documents state
 */

import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import type { DocumentsState, GenerateDocumentRequest } from '../types';
import { documentsApi, ApiClientError } from '../api/client';

const initialState: DocumentsState = {
  items: [],
  loading: false,
  error: null,
  currentDocument: null,
};

/**
 * Generate document async thunk
 */
export const generateDocument = createAsyncThunk(
  'documents/generate',
  async (request: GenerateDocumentRequest, { rejectWithValue }) => {
    try {
      const response = await documentsApi.generate(request);
      return response.document;
    } catch (error) {
      if (error instanceof ApiClientError) {
        return rejectWithValue(error.message);
      }
      return rejectWithValue('Failed to generate document');
    }
  }
);

/**
 * Fetch history async thunk
 */
export const fetchHistory = createAsyncThunk(
  'documents/fetchHistory',
  async (
    params: { limit?: number; offset?: number; doc_type?: 'email' | 'report' } = {},
    { rejectWithValue }
  ) => {
    try {
      const response = await documentsApi.getHistory(params);
      return response.documents;
    } catch (error) {
      if (error instanceof ApiClientError) {
        return rejectWithValue(error.message);
      }
      return rejectWithValue('Failed to fetch history');
    }
  }
);

const documentsSlice = createSlice({
  name: 'documents',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    clearCurrentDocument: (state) => {
      state.currentDocument = null;
    },
  },
  extraReducers: (builder) => {
    // Generate document
    builder.addCase(generateDocument.pending, (state) => {
      state.loading = true;
      state.error = null;
    });
    builder.addCase(generateDocument.fulfilled, (state, action) => {
      state.loading = false;
      state.currentDocument = action.payload;
      state.items.unshift(action.payload);
      state.error = null;
    });
    builder.addCase(generateDocument.rejected, (state, action) => {
      state.loading = false;
      state.error = action.payload as string;
    });

    // Fetch history
    builder.addCase(fetchHistory.pending, (state) => {
      state.loading = true;
      state.error = null;
    });
    builder.addCase(fetchHistory.fulfilled, (state, action) => {
      state.loading = false;
      state.items = action.payload;
      state.error = null;
    });
    builder.addCase(fetchHistory.rejected, (state, action) => {
      state.loading = false;
      state.error = action.payload as string;
    });
  },
});

export const { clearError, clearCurrentDocument } = documentsSlice.actions;
export default documentsSlice.reducer;
