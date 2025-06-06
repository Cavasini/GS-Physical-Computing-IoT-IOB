# Guia Gestual com Feedback por Voz

## Descrição do Problema

Em situações emergenciais, ambientes com pouca acessibilidade, ou contextos onde a fala é inviável (como pessoas com deficiência na fala ou em locais com ruídos intensos), a comunicação por gestos pode ser essencial. No entanto, esses gestos nem sempre são compreendidos por todos ao redor, dificultando ações rápidas e efetivas.

## Visão Geral da Solução

![Exemplo](image_maos.png)


Este projeto implementa uma aplicação de visão computacional em tempo real que reconhece gestos da mão utilizando MediaPipe e fornece uma resposta de áudio em português utilizando o pyttsx3. A ideia é facilitar a comunicação através de gestos simples, especialmente em situações onde a comunicação verbal não é possível.

A aplicação reconhece quatro gestos principais:

- Punho Fechado: Parar reconhecimento
- Joinha: Confirmar que está tudo certo
- Indicador Levantado: Acionar lanterna (simulado)
- Mão Aberta: Solicitar ajuda

Quando um gesto é detectado de forma estável por alguns segundos, o sistema emite a resposta por voz correspondente.

## Tecnologias Utilizadas

- Python 3.x
- MediaPipe (para detecção de mãos)
- OpenCV (para captura e exibição da imagem da câmera)
- pyttsx3 (para síntese de voz offline)

## Como Executar o Projeto

1. Clone o repositório:

git clone https://github.com/.................
cd repositorio

2. Instale as dependências:

pip install opencv-python mediapipe pyttsx3

3. Execute o sistema:

O sistema abrirá a câmera e iniciará a detecção em tempo real. Realize um dos gestos suportados para ouvir a resposta de voz correspondente.

## Futuras Melhorias

- Suporte a múltiplas mãos
- Reconhecimento de gestos personalizados
- Integração com comandos reais (como ativar lanterna ou enviar alerta)
- Interface gráfica com botões de configuração

## Link do vídeo

## Código-fonte

## Integrantes

Lana Giulia Auada Leite  - RM551143
Matheus Cavasini Lopes -  RM97722

