import TableDropdown from './TableDropdown';
import Loader from '../Loader';

export default function TableBody(props) {
  const { data, fields, isLoading, actions, handleDetails, handleEdit, handleDelete, selectedChannel } = props;

  console.log(data);

  const renderLoadingRow = () => (
    <tr>
      <td colSpan={fields.length + 1} className='py-4 px-2 text-lg'>
        <div className='flex items-center justify-center'>
          <Loader height='50' isLoading={isLoading} />
        </div>
      </td>
    </tr>
  );

  const renderDataRow = () =>
    data?.map((item) => (
      <tr key={item.id} className='border-b dark:border-gray-700 text-center whitespace-nowrap'>
        {fields?.map((field) => {
          if (field.includes('Date')) {
            item[field] = item[field].toString().substring(0, 10);
          }

          const fieldValue = item[field];

          console.log(fieldValue);
          console.log(item);

          const renderValue = () => {
            if (fieldValue === '') {
              return <span>----</span>;
            }

            // Check if the fieldValue contains the word "channel"
            if (field.includes('channel')) {
              return <img src={`/images/${fieldValue}`} alt={fieldValue} width='80' height='80' />;
            }

            // Check if the field is 'ticker'
            if (field === 'ticker_image') {
              return <img src={`/${selectedChannel}/${fieldValue}`} alt={fieldValue} width='500' height='200' />;
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
            id={item.id}
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
