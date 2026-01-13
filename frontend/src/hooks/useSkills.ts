import { useState } from 'react';
import { API_BASE_URL } from '../constants/api';
import { useAuth } from './useAuth';

export function useSkills() {
  const { user } = useAuth();
  const [loading, setLoading] = useState(false);

  const personalizeChapter = async (chapterSlug: string, content: string): Promise<string> => {
    setLoading(true);
    try {
      const headers: Record<string, string> = {
        'Content-Type': 'application/json',
      };

      // Add authorization header only if user is authenticated
      if (user && user.token) {
        headers['Authorization'] = `Bearer ${user.token}`;
      }

      const response = await fetch(`${API_BASE_URL}/api/personalize`, {
        method: 'POST',
        headers,
        body: JSON.stringify({ chapter_slug: chapterSlug, content }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Personalization failed' }));
        throw new Error(errorData.detail || 'Personalization failed');
      }

      const data = await response.json();
      return data.personalized_content;
    } finally {
      setLoading(false);
    }
  };

  const translateChapter = async (chapterSlug: string, content: string): Promise<string> => {
    setLoading(true);
    try {
      const headers: Record<string, string> = {
        'Content-Type': 'application/json',
      };

      // Add authorization header only if user is authenticated
      if (user && user.token) {
        headers['Authorization'] = `Bearer ${user.token}`;
      }

      const response = await fetch(`${API_BASE_URL}/api/translate`, {
        method: 'POST',
        headers,
        body: JSON.stringify({ chapter_slug: chapterSlug, content }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Translation failed' }));
        throw new Error(errorData.detail || 'Translation failed');
      }

      const data = await response.json();
      return data.translated_content;
    } finally {
      setLoading(false);
    }
  };

  return { personalizeChapter, translateChapter, loading };
}