import React, { useState } from 'react';
import Layout from '@theme-original/DocItem/Layout';
import { PersonalizeButton } from '../../components/PersonalizeButton';
import { TranslateButton } from '../../components/TranslateButton';
import { ChatWidget } from '../../components/ChatWidget';
import { useAuth } from '../../hooks/useAuth';

export default function LayoutWrapper(props) {
  const [content, setContent] = useState(null);
  const { isAuthenticated } = useAuth();

  // Extract original content from props
  const originalContent = props.content?.metadata?.unversionedId || props.content?.metadata?.title || '';

  const handleContentChange = (newContent) => {
    setContent(newContent);
  };

  return (
    <>
      {isAuthenticated && (
        <div style={{ marginBottom: '20px', padding: '10px', backgroundColor: '#f9f9f9', borderRadius: '5px' }}>
          <PersonalizeButton
            chapterSlug={props.content?.metadata?.slug || 'unknown'}
            originalContent={originalContent}
            onContentChange={handleContentChange}
          />
          <TranslateButton
            chapterSlug={props.content?.metadata?.slug || 'unknown'}
            originalContent={originalContent}
            onContentChange={handleContentChange}
          />
        </div>
      )}

      {content ? (
        <div className="markdown">
          {content}
        </div>
      ) : (
        <Layout {...props} />
      )}

      <ChatWidget />
    </>
  );
}