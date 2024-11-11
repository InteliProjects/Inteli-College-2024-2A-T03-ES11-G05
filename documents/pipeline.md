# Pipeline de CI/CD

## Introdução

O pipeline de CI/CD é uma prática de desenvolvimento de software que visa automatizar o processo de entrega de software. A sigla CI/CD significa Continuous Integration/Continuous Delivery, ou seja, Integração Contínua e Entrega Contínua.

## Workflows

Arquivos:
- [pipeline.yml](.github/workflows/pipeline.yml)
- [api-tests.yml](.github/workflows/api-test.yml)

## Esteira de CI
A pipeline de Integração Contínua (CI) deste projeto é implementada utilizando o GitHub Actions, e sua principal função é garantir a qualidade do código através de testes automatizados. Ela executa testes unitários tanto na API quanto no processo de ETL da aplicação, assegurando que cada parte do sistema esteja funcionando conforme o esperado. Esses testes são realizados em ambientes isolados, sem dependências externas, para evitar interferências que possam comprometer a integridade dos resultados. A pipeline é acionada automaticamente sempre que uma nova Pull Request (PR) é aberta nas branches de desenvolvimento, UAT ou main, permitindo a identificação rápida de problemas antes que o código seja integrado às versões principais do projeto.

A utilização do GitHub Actions permite maior flexibilidade e automação, além de integração nativa com o fluxo de versionamento e colaboração no GitHub. Esse processo contínuo ajuda a manter a estabilidade do projeto e a garantir que as mudanças introduzidas não comprometam as funcionalidades existentes.

## Esteira de CD
A pipeline de Entrega Contínua (CD) deste projeto também é implementada utilizando o GitHub Actions, sendo responsável por automatizar o processo de build, armazenamento e deploy da aplicação. Durante o processo de CD, uma imagem Docker é construída e armazenada no Amazon Elastic Container Registry (ECR), garantindo que a aplicação esteja sempre preparada para ser implementada com uma versão consistente e controlada.

Após a construção da imagem, o deploy é realizado automaticamente em uma instância EC2 na AWS, onde a aplicação é executada em um ambiente de homologação. Essa pipeline é acionada quando uma PR é aberta ou mesclada nas branches UAT ou main, assegurando que o código que passou por testes rigorosos esteja apto para ser implantado. Esse processo contínuo permite que o time entregue atualizações de forma ágil e segura, minimizando riscos e garantindo a estabilidade em produção.

A integração do GitHub Actions com os serviços da AWS, como ECR e EC2, torna o processo altamente automatizado, permitindo uma entrega contínua eficiente e sem intervenção manual, o que acelera o ciclo de desenvolvimento e implementação de novas funcionalidades.
## Tecnologias
**GitHub Actions:**

 GitHub Actions é uma plataforma de automação e CI/CD que permite executar workflows automatizados diretamente no repositório GitHub. Com Actions, você pode automatizar, personalizar e executar seus processos de desenvolvimento de software diretamente no repositório. Isso inclui tarefas como integração contínua e entrega contínua de aplicações e atualizações de infraestrutura.

**Docker:**

Docker é uma plataforma de conteinerização que permite aos desenvolvedores empacotar aplicações em contêineres — ambientes leves, portáteis e auto-suficientes que contêm tudo o que a aplicação precisa para rodar. Isso simplifica o deployment em diferentes ambientes de computação.

**AWS (Amazon Web Services):** 

AWS é um provedor de serviços de nuvem que oferece uma vasta gama de infraestruturas como serviço (IaaS), plataforma como serviço (PaaS) e pacotes de software como serviço (SaaS). Na pipeline, a AWS é utilizada como a plataforma de hospedagem para onde o Terraform provisiona e gerencia a infraestrutura necessária para a aplicação.