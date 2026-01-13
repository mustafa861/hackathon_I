import React, { useState } from 'react';
import Layout from '@theme-original/DocItem/Layout';
import { PersonalizeButton } from '../../components/PersonalizeButton';
import { TranslateButton } from '../../components/TranslateButton';
import { ChatWidget } from '../../components/ChatWidget';
import { useAuth } from '../../hooks/useAuth';

export default function LayoutWrapper(props) {
  const [content, setContent] = useState(null);
  const { isAuthenticated } = useAuth();

  // Extract chapter slug and original content from props
  const originalContent = props.content?.metadata?.unversionedId || props.content?.metadata?.title || '';
  const chapterSlug = props.content?.metadata?.unversionedId || props.content?.metadata?.id || 'unknown';

  const handleContentChange = (newContent) => {
    setContent(newContent);
  };

  return (
    <>
      <div style={{ marginBottom: '20px', padding: '10px', backgroundColor: '#f9f9f9', borderRadius: '5px' }}>
        <PersonalizeButton
          chapterSlug={chapterSlug}
          originalContent={originalContent}
          onContentChange={handleContentChange}
        />
        <TranslateButton
          chapterSlug={chapterSlug}
          originalContent={originalContent}
          onContentChange={handleContentChange}
        />
      </div>

      <Layout {...props} />

      <ChatWidget />
    </>
  );
}