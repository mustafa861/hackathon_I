import React from 'react';
import OriginalLayout from '@theme-original/DocItem/Layout';
import PersonalizationButton from '@site/src/components/PersonalizationButton';
import TranslationButton from '@site/src/components/TranslationButton';

export default function Layout(props) {
  const { metadata } = props.content;

  return (
    <>
      <div className="content-controls">
        <PersonalizationButton
          chapterId={metadata?.id}
        />
        <TranslationButton
          chapterId={metadata?.id}
        />
      </div>
      <OriginalLayout {...props} />
    </>
  );
}