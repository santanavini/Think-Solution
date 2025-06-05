GLOBAL SOLUTION FIAP 2025.1 - MONITORAMENTO INTELIGENTE DE CALOR

Este projeto consiste em um sistema completo de monitoramento de temperatura, umidade e pressão atmosférica, com armazenamento em banco de dados Oracle e previsão de temperatura por Machine Learning.

REQUISITOS:
- Python 3.10+
- Bibliotecas: cx_Oracle, pandas, joblib, scikit-learn
- Oracle Client instalado e configurado (ou via instant client)
- Conexão com o banco Oracle da FIAP (oracle.fiap.com.br/orcl) // ATENÇÃO: Foi utilizado dados de login e senha de um aluno, altere os dados para o seu caso necessário.

ARQUIVOS:
- monitoramento_calor.py → código principal do sistema
- modelo_previsao_treinado_3variaveis.pkl → modelo treinado para prever a temperatura
- exemplo_treino.csv → arquivo de amostra com dados reais utilizados no modelo
-INMET_CO_DF_A001_BRASILIA_07-05-2000_A_31-12-2000 → base de dados usada para treinar o modelo

COMO EXECUTAR:
1. Certifique-se de que as bibliotecas estejam instaladas.
2. Conecte-se à VPN da FIAP, se necessário.
3. Execute o arquivo monitoramento_calor.py em seu terminal.
4. Utilize o menu do sistema para cadastrar dados ou prever a temperatura com ML.

