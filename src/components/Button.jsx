import React from 'react';

export default function Button({ children, className, isLoading, ...rest }) {
  const buttonClassNames = `
    px-3 py-2 text-sm font-medium text-center text-white bg-blue-700 rounded-lg whitespace-nowrap hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800 ${
      isLoading ? 'opacity-50 cursor-not-allowed' : ''
    } ${className} `;

  return (
    <>
      <button type='submit' className={buttonClassNames} disabled={isLoading} {...rest}>
        {isLoading ? 'Loading...' : children}
      </button>
    </>
  );
}
