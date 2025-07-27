# 📤 DÉPLOIEMENT BACKEND DOXA AVEC FILEZILLA FTP

## 🎯 Guide Complet pour Uploader votre Backend sur LWS

### 📋 Prérequis
- **FileZilla Client** installé ([télécharger ici](https://filezilla-project.org/))
- **Informations FTP LWS** depuis votre panel
- **Dossier backend** préparé localement

## 🔑 1. Récupérer vos Informations FTP LWS

### Dans votre Panel LWS :
1. Connectez-vous à https://panel.lws.fr
2. Allez dans **"Hébergement" > "Gestion FTP"**
3. Notez ces informations :

```
Serveur FTP : ftp.votre-domaine.com (ou IP fournie)
Nom d'utilisateur : votre_nom_utilisateur
Mot de passe : votre_mot_de_passe_ftp
Port : 21 (standard) ou 22 (SFTP)
```

## 🌐 2. Configuration FileZilla

### Étape 1 : Ouvrir FileZilla
1. Lancez **FileZilla Client**
2. Allez dans **"Fichier" > "Gestionnaire de sites"**

### Étape 2 : Créer une Nouvelle Connexion
1. Cliquez sur **"Nouveau site"**
2. Nommez-le : `LWS - DOXA Backend`
3. Configurez :

```
Protocole : FTP (ou SFTP si disponible)
Hôte : ftp.votre-domaine.com
Port : 21
Type d'authentification : Normale
Identifiant : votre_nom_utilisateur_ftp
Mot de passe : votre_mot_de_passe_ftp
```

### Étape 3 : Tester la Connexion
1. Cliquez sur **"Connexion"**
2. Acceptez le certificat si demandé
3. Vous devriez voir les dossiers de votre hébergement

## 📁 3. Structure des Dossiers sur LWS

### Côté Serveur (Panneau droit FileZilla)
```
/ (racine)
├── www/                 ← Dossier principal du site
│   ├── index.html      ← Page d'accueil
│   ├── backend/        ← Créer ce dossier pour l'API
│   └── ...
├── logs/
└── tmp/
```

### Côté Local (Panneau gauche FileZilla)
```
d:\SITE OK\doxa-version-1-main\
├── backend/            ← Dossier à uploader
│   ├── api-lws.php
│   ├── .htaccess
│   ├── env-lws.txt
│   ├── database/
│   └── ...
```

## 🚀 4. Upload du Backend (Étape par Étape)

### Étape 1 : Naviguer vers le Bon Dossier
**Côté Serveur (droite) :**
1. Double-cliquez sur `www/`
2. Créez un dossier `backend/` (clic droit > Créer un dossier)
3. Entrez dans le dossier `backend/`

**Côté Local (gauche) :**
1. Naviguez vers `d:\SITE OK\doxa-version-1-main\backend\`

### Étape 2 : Sélectionner les Fichiers à Uploader
**Fichiers OBLIGATOIRES :**
- ✅ `api-lws.php` (API principale)
- ✅ `.htaccess` (configuration Apache)
- ✅ `env-lws.txt` (à renommer en `.env`)
- ✅ Dossier `database/` (avec schema.sql et seed.sql)

**Fichiers OPTIONNELS :**
- `test-api.php` (fichier de test)
- `logs/` (dossier des logs)
- `uploads/` (dossier des uploads)

### Étape 3 : Upload des Fichiers
1. **Sélectionnez** tous les fichiers nécessaires (Ctrl+clic)
2. **Glissez-déposez** du panneau gauche vers le panneau droit
3. **Confirmez** le transfert

### Progression du Transfert
```
api-lws.php               [████████████] 100%   
.htaccess                 [████████████] 100%
env-lws.txt              [████████████] 100%
database/schema.sql      [████████████] 100%
database/seed.sql        [████████████] 100%
```

## ⚙️ 5. Configuration Post-Upload

### Étape 1 : Renommer le Fichier de Configuration
1. **Clic droit** sur `env-lws.txt`
2. **"Renommer"** en `.env`
3. **Confirmer** le renommage

### Étape 2 : Éditer le Fichier .env
1. **Clic droit** sur `.env`
2. **"Afficher/Éditer"**
3. **Modifiez** avec vos informations LWS :

```env
DB_HOST=mysql.lws-hosting.fr
DB_NAME=votre_nom_base_doxa_exacte
DB_USER=votre_utilisateur_mysql_exacte
DB_PASSWORD=votre_mot_de_passe_mysql_exacte
JWT_SECRET=cle_secrete_unique_2025_doxa_investments
APP_URL=https://votre-domaine.com
```

4. **Sauvegardez** et fermez l'éditeur
5. **Confirmez** le re-upload du fichier modifié

### Étape 3 : Créer les Dossiers Nécessaires
**Via FileZilla :**
1. **Clic droit** dans le dossier backend
2. **"Créer un dossier"**
3. Créez ces dossiers :
   - `logs/`
   - `uploads/`
   - `uploads/projects/`
   - `uploads/products/`
   - `uploads/users/`

## 🗄️ 6. Import de la Base de Données

### Méthode 1 : Via phpMyAdmin LWS
1. **Connectez-vous** à votre phpMyAdmin LWS
2. **Sélectionnez** votre base de données
3. **Onglet "Importer"**
4. **Téléchargez** `database/schema.sql` depuis votre PC
5. **Cliquez** "Exécuter"
6. **Répétez** avec `database/seed.sql`

### Méthode 2 : Via l'Upload FTP + Script
1. **Uploadez** les fichiers SQL dans le dossier `database/`
2. **Créez** un script d'import temporaire
3. **Exécutez** via navigateur puis **supprimez** le script

## 🧪 7. Tests de Fonctionnement

### Test 1 : API de Base
**URL :** `https://votre-domaine.com/backend/test-api.php`

**Réponse attendue :**
```json
{
  "success": true,
  "message": "API DOXA Investments opérationnelle",
  "server": "votre-domaine.com"
}
```

### Test 2 : Endpoint Principal
**URL :** `https://votre-domaine.com/backend/api/health`

**Réponse attendue :**
```json
{
  "status": "success",
  "message": "API DOXA opérationnelle"
}
```

### Test 3 : Connexion Base de Données
**URL :** `https://votre-domaine.com/backend/api/projects`

## 🔧 8. Résolution des Problèmes

### Erreur 500 (Internal Server Error)
```bash
Cause possible : Fichier .htaccess ou permissions
Solution : 
1. Vérifiez que .htaccess est uploadé
2. Changez les permissions (755 pour dossiers, 644 pour fichiers)
```

### Erreur de Connexion Base de Données
```bash
Cause possible : Informations incorrectes dans .env
Solution :
1. Vérifiez les informations MySQL dans votre panel LWS
2. Re-éditez le fichier .env avec les bonnes valeurs
```

### Problème CORS
```bash
Cause possible : Configuration .htaccess
Solution :
1. Vérifiez que .htaccess contient les headers CORS
2. Adaptez les domaines autorisés
```

## 📱 9. Interface FileZilla - Captures d'Écran Type

```
┌─ Panneau Local (Gauche) ─┐ ┌─ Panneau Serveur (Droite) ─┐
│ 📁 backend/              │ │ 📁 www/                     │
│   📄 api-lws.php         │ │   📁 backend/               │
│   📄 .htaccess           │ │     📄 api-lws.php         │
│   📄 env-lws.txt         │ │     📄 .htaccess           │
│   📁 database/           │ │     📄 .env                │
│     📄 schema.sql        │ │     📁 database/           │
│     📄 seed.sql          │ │     📁 logs/               │
└──────────────────────────┘ └────────────────────────────┘
```

## ✅ 10. Checklist Finale

- [ ] **Connexion FTP** établie avec succès
- [ ] **Dossier backend/** créé sur le serveur
- [ ] **Fichiers PHP** uploadés (api-lws.php, .htaccess)
- [ ] **Fichier .env** configuré avec vos données LWS
- [ ] **Dossiers uploads/** créés avec bonnes permissions
- [ ] **Base de données** importée (schema.sql + seed.sql)
- [ ] **Test API** fonctionnel
- [ ] **Frontend** configuré pour pointer vers la bonne URL

## 🎉 Félicitations !

Votre backend DOXA Investments est maintenant **déployé et opérationnel** sur LWS via FileZilla !

**URL de votre API :** `https://votre-domaine.com/backend/`

---

> 💡 **Conseil :** Sauvegardez vos paramètres FileZilla pour les futures mises à jour et gardez une copie locale de votre configuration .env !
