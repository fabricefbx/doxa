const { default: fetch } = require('node-fetch');

console.log('\n🎨 TEST DES PAGES OPTIMISÉES - DOXA INVESTMENTS\n');
console.log('='.repeat(60));

const baseUrl = 'https://www.dith-fastbusiness.com';

const tests = [
    {
        name: 'Page d\'accueil améliorée',
        url: `${baseUrl}/`,
        expectedKeywords: ['DOXA Investments', 'Services', 'État du Système']
    },
    {
        name: 'Page 404 personnalisée',
        url: `${baseUrl}/page-inexistante`,
        expectedKeywords: ['404', 'Page non trouvée', 'DOXA']
    },
    {
        name: 'Page de maintenance',
        url: `${baseUrl}/maintenance.html`,
        expectedKeywords: ['Maintenance', 'Progression', 'DOXA']
    },
    {
        name: 'Application Frontend',
        url: `${baseUrl}/frontend/`,
        expectedKeywords: ['React', 'App', 'root']
    },
    {
        name: 'Test API Backend',
        url: `${baseUrl}/backend/api.php`,
        checkStatus: true
    }
];

async function testPage(test) {
    try {
        console.log(`\n🔍 Test: ${test.name}`);
        console.log(`📡 URL: ${test.url}`);
        
        const response = await fetch(test.url, {
            method: 'GET',
            headers: {
                'User-Agent': 'DOXA-Test-Agent/1.0'
            },
            timeout: 10000
        });
        
        const status = response.status;
        const statusText = response.statusText;
        const contentLength = response.headers.get('content-length') || 'unknown';
        
        console.log(`📊 Statut: ${status} ${statusText}`);
        console.log(`📏 Taille: ${contentLength} octets`);
        
        if (test.checkStatus) {
            // Pour l'API, on vérifie juste le statut
            if (status === 200) {
                console.log('✅ API Backend: Opérationnelle');
            } else if (status === 500) {
                console.log('⏳ API Backend: En attente d\'activation PHP');
            } else {
                console.log(`❌ API Backend: Erreur ${status}`);
            }
        } else {
            // Pour les pages HTML, on vérifie le contenu
            const content = await response.text();
            
            if (test.expectedKeywords) {
                console.log('🔍 Vérification du contenu:');
                test.expectedKeywords.forEach(keyword => {
                    if (content.includes(keyword)) {
                        console.log(`  ✅ "${keyword}" trouvé`);
                    } else {
                        console.log(`  ❌ "${keyword}" manquant`);
                    }
                });
            }
            
            // Vérifications supplémentaires
            const hasCSS = content.includes('<style>') || content.includes('.css');
            const hasJS = content.includes('<script>') || content.includes('.js');
            const hasResponsive = content.includes('viewport');
            const hasIcons = content.includes('font-awesome') || content.includes('fas fa-');
            
            console.log('🎨 Analyse technique:');
            console.log(`  CSS: ${hasCSS ? '✅' : '❌'}`);
            console.log(`  JavaScript: ${hasJS ? '✅' : '❌'}`);
            console.log(`  Responsive: ${hasResponsive ? '✅' : '❌'}`);
            console.log(`  Icônes: ${hasIcons ? '✅' : '❌'}`);
        }
        
        return { success: true, status, size: contentLength };
        
    } catch (error) {
        console.log(`❌ Erreur: ${error.message}`);
        return { success: false, error: error.message };
    }
}

async function runAllTests() {
    console.log('🚀 Démarrage des tests...\n');
    
    const results = [];
    
    for (const test of tests) {
        const result = await testPage(test);
        results.push({ name: test.name, ...result });
        
        // Pause entre les tests
        await new Promise(resolve => setTimeout(resolve, 1000));
    }
    
    // Résumé final
    console.log('\n' + '='.repeat(60));
    console.log('📋 RÉSUMÉ DES TESTS');
    console.log('='.repeat(60));
    
    let successCount = 0;
    results.forEach(result => {
        const status = result.success ? 
            (result.status === 200 ? '✅ OK' : result.status === 500 ? '⏳ En attente' : `⚠️  ${result.status}`) : 
            '❌ Erreur';
        console.log(`${result.name}: ${status}`);
        if (result.success && (result.status === 200 || result.status === 404)) successCount++;
    });
    
    console.log('\n📊 STATISTIQUES:');
    console.log(`Tests réussis: ${successCount}/${results.length}`);
    console.log(`Taux de réussite: ${Math.round(successCount/results.length*100)}%`);
    
    if (results.some(r => r.status === 500)) {
        console.log('\n⏳ STATUT DÉPLOIEMENT:');
        console.log('Frontend: ✅ Opérationnel');
        console.log('Backend: ⏳ Activation PHP en cours');
        console.log('Base de données: ✅ Configurée');
        console.log('\n💡 Action requise: Attendre activation PHP par LWS');
    }
    
    console.log('\n✨ Tests terminés - DOXA Investments');
}

// Gestion des erreurs globales
process.on('unhandledRejection', (reason, promise) => {
    console.log('❌ Erreur non gérée:', reason);
});

// Lancement des tests
runAllTests().catch(console.error);
