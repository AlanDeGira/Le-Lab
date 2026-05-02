-- Schema Le Lab v2
-- Architecture : 26 portfolios, 1 prénom/portfolio, 10 publieurs + 1 admin

CREATE TABLE portfolios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    numero INTEGER UNIQUE NOT NULL,
    lettre TEXT NOT NULL,
    prenom TEXT NOT NULL,
    business_manager_id TEXT,
    proxy TEXT,
    statut TEXT DEFAULT 'en_creation' 
        CHECK(statut IN ('en_creation', 'actif', 'suspendu')),
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE comptes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    portfolio_id INTEGER NOT NULL,
    email TEXT NOT NULL,
    suffixe TEXT NOT NULL,                      -- reel, story, content, strateur...
    mot_de_passe TEXT NOT NULL,                 -- Prénom1! ou Prénom.admin1!
    nom_page TEXT,                              -- Nom de la page Facebook
    reseau TEXT NOT NULL 
        CHECK(reseau IN ('facebook_page', 'instagram', 'tiktok')),
    pseudo_instagram TEXT,                      -- Pseudo Instagram (si applicable)
    statut TEXT DEFAULT 'en_attente'
        CHECK(statut IN ('en_attente', 'creation', 'actif', 'bloque', 'shadowban', 'a_verifier')),
    role TEXT DEFAULT 'publication'
        CHECK(role IN ('publication', 'admin')),
    date_de_naissance TEXT DEFAULT '1990-01-01',
    derniere_verification DATETIME,
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(email, reseau),
    FOREIGN KEY (portfolio_id) REFERENCES portfolios(id)
);

CREATE TABLE videos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fichier TEXT NOT NULL,
    chemin TEXT NOT NULL,
    duree_secondes INTEGER,
    theme TEXT,
    description TEXT,
    portfolio_id INTEGER,
    nombre_publications INTEGER DEFAULT 0,
    date_ajout DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (portfolio_id) REFERENCES portfolios(id)
);

CREATE TABLE publications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    compte_id INTEGER NOT NULL,
    video_id INTEGER NOT NULL,
    date_prevue DATETIME NOT NULL,
    date_reelle DATETIME,
    statut TEXT DEFAULT 'planifie'
        CHECK(statut IN ('planifie', 'succes', 'echec', 'annule')),
    message_erreur TEXT,
    FOREIGN KEY (compte_id) REFERENCES comptes(id),
    FOREIGN KEY (video_id) REFERENCES videos(id)
);

CREATE TABLE logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    niveau TEXT NOT NULL CHECK(niveau IN ('info', 'warning', 'error', 'critical')),
    source TEXT NOT NULL,
    message TEXT NOT NULL,
    details TEXT,
    date DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Index
CREATE INDEX idx_comptes_portfolio ON comptes(portfolio_id);
CREATE INDEX idx_comptes_statut ON comptes(statut);
CREATE INDEX idx_comptes_reseau ON comptes(reseau);
CREATE INDEX idx_comptes_role ON comptes(role);
CREATE INDEX idx_publications_date ON publications(date_prevue);
CREATE INDEX idx_publications_compte ON publications(compte_id);
CREATE INDEX idx_logs_date ON logs(date);
CREATE INDEX idx_logs_niveau ON logs(niveau);

-- Vue état global
CREATE VIEW vue_etat_global AS
SELECT 
    (SELECT COUNT(*) FROM comptes) as total_comptes,
    (SELECT COUNT(*) FROM comptes WHERE statut = 'actif') as comptes_actifs,
    (SELECT COUNT(*) FROM comptes WHERE statut = 'bloque') as comptes_bloques,
    (SELECT COUNT(*) FROM comptes WHERE statut = 'shadowban') as comptes_shadowban,
    (SELECT COUNT(*) FROM comptes WHERE statut = 'a_verifier') as comptes_a_verifier,
    (SELECT COUNT(*) FROM portfolios) as total_portfolios,
    (SELECT COUNT(*) FROM portfolios WHERE statut = 'actif') as portfolios_actifs,
    (SELECT COUNT(*) FROM publications WHERE statut = 'succes') as pubs_reussies,
    (SELECT COUNT(*) FROM publications WHERE statut = 'echec') as pubs_echouees;

-- Vue détail par portfolio
CREATE VIEW vue_portfolio_detail AS
SELECT 
    p.id, p.numero, p.lettre, p.prenom, p.statut as statut_portfolio,
    COUNT(c.id) as total_comptes,
    SUM(CASE WHEN c.role = 'admin' THEN 1 ELSE 0 END) as admins,
    SUM(CASE WHEN c.statut = 'actif' THEN 1 ELSE 0 END) as actifs,
    SUM(CASE WHEN c.statut = 'bloque' THEN 1 ELSE 0 END) as bloques,
    SUM(CASE WHEN c.reseau = 'facebook_page' THEN 1 ELSE 0 END) as facebook,
    SUM(CASE WHEN c.reseau = 'instagram' THEN 1 ELSE 0 END) as instagram,
    SUM(CASE WHEN c.reseau = 'tiktok' THEN 1 ELSE 0 END) as tiktok
FROM portfolios p
LEFT JOIN comptes c ON p.id = c.portfolio_id
GROUP BY p.id;
