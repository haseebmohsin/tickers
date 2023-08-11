import Header from '../Header';

function MainLayout({ children }) {
  return (
    <>
      <Header />

      <main>{children}</main>
    </>
  );
}

export default MainLayout;
