import TableDropdown from './TableDropdown';
import Loader from '../Loader';

export default function TableBody(props) {
  const { data, fields, isLoading, actions, handleDetails, handleEdit, handleDelete } = props;

  const renderLoadingRow = () => (
    <tr className=''>
      <td colSpan={fields.length + 1} className='py-4 px-2 text-lg'>
        <div className='flex items-center justify-center'>
          <Loader height='50' isLoading={isLoading} />
        </div>
      </td>
    </tr>
  );

  const renderDataRow = () =>
    data?.map((item) => (
      <tr key={item._id} className='border-b dark:border-gray-700 text-center whitespace-nowrap'>
        {fields?.map((field) => {
          if (field.includes('uploadDate')) {
            item[field] = item[field].toString().substring(0, 10);
          }

          const fieldValue = item[field];

          const renderValue = () => {
            if (fieldValue === '') {
              return <span>----</span>;
            }

            // Check if the fieldValue contains the word "channel"
            if (field.includes('streamName')) {
              return <img src={`/logos/${fieldValue}.png`} alt={fieldValue} width='40' height='40' />;
            }

            // Check if the field is 'ticker'
            if (field === 'tickerImage') {
              return <img src={`data:image/jpeg;base64,${fieldValue}`} alt='Ticker' width='600' height='300' />;
            }

            return fieldValue;
          };

          return (
            <td key={field} className='p-2'>
              {renderValue()}
            </td>
          );
        })}

        {actions && (
          <TableDropdown
            id={item._id}
            actions={actions}
            handleDetails={handleDetails}
            handleEdit={handleEdit}
            handleDelete={handleDelete}
          />
        )}
      </tr>
    ));

  const renderEmptyRow = () => (
    <tr>
      <td colSpan={fields.length + 1} className='py-4 px-2 text-lg'>
        No data found
      </td>
    </tr>
  );

  return <tbody>{isLoading ? renderLoadingRow() : data?.length > 0 ? renderDataRow() : renderEmptyRow()}</tbody>;
}
