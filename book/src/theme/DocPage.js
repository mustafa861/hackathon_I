import React, { useState } from 'react';
import OriginalDocPage from '@theme-original/DocPage';
import PersonalizationButton from '@site/src/components/PersonalizationButton';

export default function DocPage(props) {
  const [currentContent, setCurrentContent] = useState(null);
  const [originalContent, setOriginalContent] = useState(null);

  // Extract the content from the doc page - this is a simplified approach
  // In a real implementation, we might need to traverse the children to find content
  const docContent = props.content;
  const metadata = docContent.metadata;

  const handlePersonalize = (personalizedContent) => {
    setCurrentContent(personalizedContent);
  };

  const handleReset = () => {
    setCurrentContent(null);
  };

  // Pass the content and handlers to the personalization button
  const personalizationComponent = (
    <PersonalizationButton
      content={originalContent || ""}
      chapterId={metadata?.id}
      onPersonalize={handlePersonalize}
      onReset={handleReset}
    />
  );

  // Clone the content component to potentially inject personalized content
  const modifiedContent = React.cloneElement(props.content, {
    ...props.content.props,
    // This is a simplified approach - in reality, you might need to modify the content rendering differently
    // depending on how Docusaurus structures its content components
  });

  return (
    <>
      {personalizationComponent}
      <OriginalDocPage {...props} content={modifiedContent} />
    </>
  );
}