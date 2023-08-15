import React from 'react';

export default function Select({ onChange }) {
  const handleChange = (event) => {
    const selectedValue = event.target.value;
    onChange(selectedValue);
  };

  return (
    <div className='w-1/2'>
      <select
        id='countries'
        className='bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
        onChange={handleChange}>
        <option defaultValue>Choose Channel</option>
        <option value='Geo'>Geo News</option>
        <option value='Ary'>Ary News</option>
        <option value='Samaa'>Samaa News</option>
        <option value='Dunya'>Dunya News</option>
        <option value='Hum'>Hum News</option>
        <option value='Express'>Express News</option>
      </select>
    </div>
  );
}
