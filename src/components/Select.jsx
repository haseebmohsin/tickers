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
        <option value='geo_ticker'>Geo News</option>
        <option value='ary_ticker'>Ary News</option>
        <option value='samma_ticker'>Samma News</option>
        <option value='dunya_ticker'>Dunya News</option>
        <option value='hum_ticker'>Hum News</option>
        <option value='express_ticker'>Express News</option>
      </select>
    </div>
  );
}
