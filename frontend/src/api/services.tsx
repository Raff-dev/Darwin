import API_URLS from './config';

export const getDocuments = async () => {
  const response = await fetch(API_URLS.DOCUMENTS);
  if (!response.ok) {
    throw new Error(`Failed to fetch documents: ${response.statusText}`);
  }
  return response.json();
};

export const createDocument = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(API_URLS.DOCUMENTS, {
    method: 'POST',
    body: formData,
  });
  if (!response.ok) {
    throw new Error(`Failed to create document: ${response.statusText}`);
  }
  return response.json();
};
