import React from 'react';
import Error from './pages/Error';
import Home from './pages/Home';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { CssBaseline } from '@mui/material';

const darkTheme = createTheme({
  palette: {
    mode: 'dark'
  },
});

const App = () => {
	return (
		<ThemeProvider theme={darkTheme}>
			<CssBaseline />	
			<BrowserRouter>
				<Routes>
						<Route path='/' element={<Home />}/>
						<Route path='*' element={<Error />} />
				</Routes>		
			</BrowserRouter>
		</ThemeProvider>
  );
};

export default App;
