import API_URLS from './config';

export interface Document {
  id: number;
  filename: string;
}

export const getDocument = async (id: number): Promise<Document> => {
  const response = await fetch(`${API_URLS.DOCUMENTS}/${id}`);
  if (!response.ok) {
      throw new Error(`Failed to fetch document: ${response.statusText}`);
  }
  return response.json();
};

export const getDocuments = async (): Promise<Document[]> => {
  const response = await fetch(API_URLS.DOCUMENTS);
  if (!response.ok) {
    throw new Error(`Failed to fetch documents: ${response.statusText}`);
  }
  return response.json();
};

export const createDocument = async (file: File): Promise<Document> => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('filename', file.name);

  const response = await fetch(API_URLS.DOCUMENTS, {
    method: 'POST',
    body: formData,
  });
  if (!response.ok) {
    throw new Error(`Failed to create document: ${response.statusText}`);
  }
  return response.json();
};

export const deleteDocument = async (id: number): Promise<Document> => {
  const response = await fetch(`${API_URLS.DOCUMENTS}/${id}`, {
      method: 'DELETE',
  });
  if (!response.ok) {
      throw new Error(`Failed to delete document: ${response.statusText}`);
  }
  return response.json();
};
