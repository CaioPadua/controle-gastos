const express = require('express');
const cors = require('cors');
const app = express();

// Habilitar CORS para todas as rotas
app.use(cors());

const contas = {
    "Janeiro": [
        { descricao: "Conta de Luz", valor: 150.75, data_vencimento: "2024-01-15", parcelas: 1 },
        { descricao: "Conta de Água", valor: 75.30, data_vencimento: "2024-01-20", parcelas: 1 }
    ],

    "Fevereiro": [
        { descricao: "Conta de Luz", valor: 150.75, data_vencimento: "2024-01-15", parcelas: 1 },
        { descricao: "Conta de Água", valor: 75.30, data_vencimento: "2024-01-20", parcelas: 1 }
    ],

    "Março": [

    ],

    "Abril": [

    ],

    "Maio": [

    ],

    "Junho": [

    ],

    "Julho": [

    ],

    "Agosto": [

    ],

    "Setembro": [

    ],

    "Outubro": [

    ],

    "Novembro": [

    ],

    "Dezembro": [

    ],
};

app.get('/contas', (req, res) => {
    const mes = req.query.mes;
    if (contas[mes]) {
        res.json(contas[mes]);
    } else {
        res.status(404).json([]);
    }
});

app.listen(3000, () => {
    console.log('Servidor rodando na porta 3000');
});