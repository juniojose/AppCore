// Componente Header
const Header = () => {
    // Menus mockados (substituir por dados do backend no futuro)
    const menus = [
        { menuNome: 'Home', menuTemplate: 'home' },
        { menuNome: 'Dashboard', menuTemplate: 'dashboard' },
        { menuNome: 'Configurações', menuTemplate: 'settings' },
    ];

    // Log para depurar clique no toggler
    const handleTogglerClick = () => {
        console.log('Navbar toggler clicado');
        const navbar = document.getElementById('navbarNav');
        console.log('Estado do navbar:', navbar.classList.contains('show') ? 'Visível' : 'Oculto');
    };

    return (
        <header className="custom-header">
            <div className="top-bar d-flex justify-content-between align-items-center">
                <img
                    src="/static/logo.png"
                    alt="Logo"
                    className="img-fluid logo-img"
                />
                <div className="d-flex align-items-center">
                    <a href="/search" className="text-white" style={{ marginRight: '15px' }}>
                        <i className="bi bi-search" style={{ fontSize: '1.5rem' }}></i>
                    </a>
                    <a href="/profile" className="text-white">
                        <i className="bi bi-person-circle" style={{ fontSize: '1.5rem' }}></i>
                    </a>
                    <a href="/auth/logout" className="text-white" style={{ marginLeft: '15px' }}>
                        <i className="bi bi-box-arrow-right" style={{ fontSize: '1.5rem' }}></i>
                    </a>
                </div>
            </div>
            <nav className="navbar navbar-expand-lg navbar-dark">
                <div className="container-fluid">
                    <button
                        className="navbar-toggler"
                        type="button"
                        data-bs-toggle="collapse"
                        data-bs-target="#navbarNav"
                        aria-controls="navbarNav"
                        aria-expanded="false"
                        aria-label="Toggle navigation"
                        onClick={handleTogglerClick}
                    >
                        <span className="navbar-toggler-icon"></span>
                    </button>
                    <div className="navbar-collapse" id="navbarNav">
                        <ul className="navbar-nav">
                            {menus.map((menu, index) => (
                                <li className="nav-item" key={index}>
                                    <a
                                        className="nav-link"
                                        href={menu.menuTemplate === 'home' ? '/' : `/menu/${menu.menuTemplate}`}
                                    >
                                        {menu.menuNome}
                                    </a>
                                </li>
                            ))}
                        </ul>
                    </div>
                </div>
            </nav>
        </header>
    );
};

// Componente FlashMessages (simulação, será integrado com backend)
const FlashMessages = () => {
    // Mock de mensagens flash
    const [messages, setMessages] = React.useState([
        { category: 'success', message: 'Bem-vindo ao AppCore!' },
    ]);

    return (
        <div className="container mt-3">
            {messages.map((msg, index) => (
                <div
                    key={index}
                    className={`alert alert-${msg.category} alert-dismissible fade show`}
                    role="alert"
                >
                    {msg.message}
                    <button
                        type="button"
                        className="btn-close"
                        data-bs-dismiss="alert"
                        aria-label="Close"
                        onClick={() => setMessages(messages.filter((_, i) => i !== index))}
                    ></button>
                </div>
            ))}
        </div>
    );
};

// Componente Main
const Main = () => {
    return (
        <main className="flex-grow-1 d-flex flex-column align-items-start p-3">
            <FlashMessages />
            <h1 className="text-2xl font-bold">Bem-vindo ao AppCore</h1>
            <p>Esta é a página inicial da aplicação.</p>
        </main>
    );
};

// Componente Footer
const Footer = () => {
    return (
        <footer className="custom-footer text-center mt-auto py-3">
            © 2025 FzPy
        </footer>
    );
};

// Componente Principal
const App = () => {
    // Estender sessão a cada 5 minutos (simulação)
    React.useEffect(() => {
        console.log('Aplicativo React renderizado');
        const interval = setInterval(() => {
            fetch('/extend_session', { method: 'POST' })
                .then(() => console.log('Sessão estendida'))
                .catch(err => console.error('Erro ao estender sessão:', err));
        }, 5 * 60 * 1000); // 5 minutos
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="d-flex flex-column min-vh-100">
            <Header />
            <Main />
            <Footer />
        </div>
    );
};

// Renderizar o aplicativo
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);