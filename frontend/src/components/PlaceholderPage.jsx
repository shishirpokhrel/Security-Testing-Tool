const Page = ({ title }) => (
    <div className="fade-in">
        <h1 style={{ fontSize: '32px', marginBottom: '16px' }}>{title}</h1>
        <div className="card">
            <p style={{ color: 'var(--text-secondary)' }}>Module initialized. Ready for implementation.</p>
        </div>
    </div>
);
export default Page;
