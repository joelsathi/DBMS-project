import React from 'react';
import { Helmet } from 'react-helmet';

type Props = {
  title?: string;
  description?: string;
  keywords?: string;
};

const Meta = ({
  title = 'Welcome To Thulasi Stores',
  description = 'the best online store :)',
  keywords,
}: Props) => {
  return (
    <Helmet>
      <title>{title}</title>
      <meta name='description' content={description} />
      <meta name='keyword' content={keywords} />
    </Helmet>
  );
};

export default Meta;
