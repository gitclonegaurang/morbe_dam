// import { useEffect, useState } from 'react';
// import axios from 'axios';
// import * as XLSX from 'xlsx';
// import { initGTM } from './gtm';

// function App() {
//   const [data, setData] = useState([]);
//   // useEffect(() => {
//   //   initGTM(process.env.REACT_APP_GTM_ID); // Replace with your Google Tag Manager ID
//   // }, []);

//   const fetchData = async () => {
//     try {
//       const response = await axios.get('http://localhost:5000/data'); // Adjust port if necessary
      
//       // Extract the latest 5 entries
//       const latestEntries = response.data;
      
//       // Update state with latest entries
//       setData(latestEntries);
//     } catch (error) {
//       console.error('Error fetching data:', error);
//     }
//   };

//   const scrapeData = async () => {
//     try {
//       await axios.get('http://localhost:5000/scrape');
//       fetchData(); // Fetch data after scraping
//     } catch (error) {
//       console.error('Error scraping data:', error);
//     }
//   };

//   useEffect(() => {
//     scrapeData(); // Scrape data on initial load
//   }, []);

//   const downloadExcel = () => {
//     const ws = XLSX.utils.json_to_sheet(data);
//     const wb = XLSX.utils.book_new();
//     XLSX.utils.book_append_sheet(wb, ws, 'Data');
//     XLSX.writeFile(wb, 'water_levels.xlsx');
//   };

//   return (
//     <div className="container">
//       <h1 className="text-3xl font-bold mb-4">Dam Water Levels</h1>
//       <button onClick={downloadExcel} className="button">Download Excel</button>
//       <table className="table">
//         <thead>
//           <tr>
//             <th>Date</th>
//             <th>Today's Rainfall</th>
//             <th>Up-to-date Rainfall</th>
//             <th>Full Supply Level</th>
//             <th>Today's Dam Level</th>
//             <th>Gross Storage</th>
//             <th>Today's Gross Storage</th>
//           </tr>
//         </thead>
//         <tbody>
//           {data.map((item, index) => (
//             <tr key={index}>
//               <td>{item.date}</td>
//               <td>{item.todays_rainfall}</td>
//               <td>{item.upto_date_rainfall}</td>
//               <td>{item.full_supply_level}</td>
//               <td>{item.todays_dam_level}</td>
//               <td>{item.gross_storage}</td>
//               <td>{item.todays_gross_storage}</td>
//             </tr>
//           ))}
//         </tbody>
//       </table>
//     </div>
//   );
// }

// export default App;
import { useEffect, useState } from 'react';
import axios from 'axios';
import * as XLSX from 'xlsx';
// import TagManager from 'react-gtm-module';

function App() {
  const [data, setData] = useState([]);

  // useEffect(() => {
  //   const gtmId = process.env.REACT_APP_GTM_ID;
  //   if (gtmId) {
  //     initGTM(gtmId);
  //   } else {
  //     console.error('GTM ID is not defined in the environment variables.');
  //   }
  // }, []);
  const fetchData = async () => {
    try {
      const response = await axios.get('http://localhost:5000/data'); // Adjust port if necessary
      setData(response.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  const scrapeData = async () => {
    try {
      await axios.get('http://localhost:5000/scrape');
      fetchData(); // Fetch data after scraping
    } catch (error) {
      console.error('Error scraping data:', error);
    }
  };

  useEffect(() => {
    fetchData(); // Initial data fetch
  }, []);

  const downloadExcel = () => {
    const ws = XLSX.utils.json_to_sheet(data);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Data');
    XLSX.writeFile(wb, 'water_levels.xlsx');
  };

  return (
    <div className="container">
      <h1 className="text-3xl font-bold mb-4">Morbe Dam Water Level</h1>
      <p> We wish to remind the citizens of Navi Mumbai of our heavy reliance on a single water structure for our daily needs. As this vital resource diminishes, it is crucial to transition towards sustainable living. Let us make conscientious decisions in our water usage and explore alternative water conservation methods.</p>
      <button onClick={downloadExcel} className="button">Download Excel</button>
      <br />
      <button onClick={scrapeData} className="button">Get Updated Data</button>
      <table className="table">
        <thead>
          <tr>
            <th>Date</th>
            <th>Rainfall(in MM)</th>
            <th>Up-to-date Rainfall(in MM)</th>
            <th>Full Supply Level</th>
            <th>Today's Dam Level</th>
            <th>Gross Storage</th>
            <th>Today's Gross Storage</th>
            <th>% of Gross Storage</th>
          </tr>
        </thead>
        <tbody>
          {data.map((item, index) => (
            <tr key={index}>
              <td>{item.date}</td>
              <td>{item.todays_rainfall}</td>
              <td>{item.upto_date_rainfall}</td>
              <td>{item.full_supply_level}</td>
              <td>{item.todays_dam_level}</td>
              <td>{item.gross_storage}</td>
              <td>{item.todays_gross_storage}</td>
              <td>{((item.todays_gross_storage / item.gross_storage) * 100).toFixed(2)} %</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
