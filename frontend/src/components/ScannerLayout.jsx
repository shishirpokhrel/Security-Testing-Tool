const ScannerLayout = ({ title, description, badge, children }) => {
    return (
        <div className="fade-in">
            <header style={{ marginBottom: '32px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '8px' }}>
                    <h1 style={{ fontSize: '32px', margin: 0 }}>{title}</h1>
                    {badge && (
                        <span style={{
                            background: 'rgba(0, 255, 148, 0.1)',
                            color: 'var(--primary-color)',
                            padding: '4px 12px',
                            borderRadius: '20px',
                            fontSize: '12px',
                            fontWeight: '600'
                        }}>
                            {badge}
                        </span>
                    )}
                </div>
                <p style={{ color: 'var(--text-secondary)', maxWidth: '600px', lineHeight: '1.6' }}>
                    {description}
                </p>
            </header>

            {children}
        </div>
    );
};

export default ScannerLayout;
