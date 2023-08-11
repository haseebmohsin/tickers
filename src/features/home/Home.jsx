import { useEffect, useState } from 'react';
import history from '../../navigation';
import SearchBar from '../../components/SearchBar';
import Select from '../../components/Select';
import Button from '../../components/Button';
import makeRequest from '../../utils/makeRequest.js';
import { data } from '../../data/data';
import ToggleSwitch from '../../components/ToggleSwitch';
import Table from '../../components/tables/Table';
import TableHead from '../../components/tables/TableHead';
import TableBody from '../../components/tables/TableBody';

import MyDatepicker from '../../components/MyDatepicker';
import MyTimepicker from '../../components/MyTimepicker';

const entries = ['id', 'Channel', 'Ticker', 'Date', 'Time'];
const fields = ['channel', 'ticker', 'date', 'time'];
const actions = ['Details'];

function Home() {
  // const { data: session, status } = useSession();
  const [searchTerm, setSearchTerm] = useState('');
  const [isTickersDataLoading, setIsTickersDataLoading] = useState(false);
  const [selectedChannel, setSelectedChannel] = useState('');
  const [newsData, setNewsData] = useState([]);

  const onSearch = (e) => {
    e.preventDefault();

    if (searchTerm === '') {
      setNewsData(data);
    }

    if (searchTerm === 'سرکاری') {
      const filteredData = data.filter((item) => item.id === 2);
      setNewsData(filteredData);
    }

    if (searchTerm === 'صدر') {
      const filteredData = data.filter((item) => item.id === 5);
      setNewsData(filteredData);
    }
  };

  const handleToggleOn = () => {
    setIsTickersDataLoading(true);

    setInterval(async () => {
      try {
        const response = await makeRequest({ path: `${selectedChannel}` });

        console.log(response.all_tickers);

        setNewsData(response.all_tickers);

        // setNewsData(
        //   response.all_tickers.map((ticker, index) => ({
        //     id: index + 1,
        //     channel: 'geo-news.png',
        //     ticker: ticker,
        //     date: response.date,
        //     time: response.timedata[index],
        //   }))
        // );
      } catch (error) {
        console.log(error);
      } finally {
        setIsTickersDataLoading(false);
      }
    }, 7000);
  };

  // single inventory record details
  const handleDetails = async (id) => {
    history.push(`/ticker/${id}`);
  };

  return (
    <>
      <div className='flex justify-center p-6 mt-16 max-w-7xl mx-auto'>
        <div className='relative dark:bg-gray-800 overflow-hidden'>
          <div className='flex flex-col gap-6 p-1 mb-3'>
            <div className='flex flex-col md:flex-row justify-center items-center gap-2'>
              <div className='flex gap-2 w-full'>
                <SearchBar searchTerm={searchTerm} setSearchTerm={setSearchTerm} onSearch={onSearch} />
              </div>

              <div className='flex items-center justify-between gap-4 w-full'>
                <Select onChange={(selectedValue) => setSelectedChannel(selectedValue)} />

                <ToggleSwitch onToggleOn={handleToggleOn} />
              </div>
            </div>

            <div className='flex flex-col md:flex-row justify-center md:items-center items-end gap-4'>
              {/* Date range */}
              <div className='flex gap-2 w-full'>
                {/* <MyDatepicker title='Start Date' />
                <MyDatepicker title='End Date' /> */}
              </div>

              {/* Time range */}
              <div className='flex gap-2 w-full'>
                {/* <MyTimepicker title='Start Time' />
                <MyTimepicker title='End Time' /> */}
              </div>

              <div>
                <Button onClick={() => console.log('clicking apply')}>Apply</Button>
              </div>
            </div>
          </div>

          <div>
            <Table>
              <TableHead entries={entries} />

              <TableBody
                isLoading={isTickersDataLoading}
                fields={fields}
                data={newsData}
                actions={actions}
                handleDetails={handleDetails}
                selectedChannel={selectedChannel}
              />
            </Table>
          </div>
        </div>
      </div>
    </>
  );
}

export default Home;
