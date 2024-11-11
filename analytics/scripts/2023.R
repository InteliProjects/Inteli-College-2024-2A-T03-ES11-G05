knitr::opts_chunk$set(echo = TRUE)

# Instalação e carregamento das bibliotecas necessárias
required_packages <- c("dplyr", "tibble", "ggplot2", "corrplot", "FactoMineR", "factoextra")
for (pkg in required_packages) {
  if (!requireNamespace(pkg, quietly = TRUE)) {
    install.packages(pkg)
  }
  library(pkg, character.only = TRUE)
}

# Começar timer
start_time <- Sys.time()

# Porcentagem do DataFrame que será amostrada
sample_frac <- 1.0

# Carregando os dados e convertendo para tibble
datasets <- list(
  ano_2024 = read.csv("./datasets/raw/2024.csv"),
  store_final = read.csv("./datasets/raw/store_final.csv"),
  target_store_final = read.csv("./datasets/raw/target_store_final.csv"),
  sku_status_dataset = read.csv2("./datasets/raw/sku_status_dataset.csv"),
  targets_salesperson_final = read.csv("./datasets/raw/targets_salesperson_final.csv"),
  sku_price = read.csv("./datasets/raw/sku_price.csv"),
  sku_dataset = read.csv2("./datasets/raw/sku_dataset.csv"),
  sku_cost = read.csv("./datasets/raw/sku_cost.csv"),
  employee_final = read.csv("./datasets/raw/employee_final.csv")
) %>% 
  lapply(as_tibble)

# Função para visualizar as primeiras linhas de cada dataset
view_head <- function(data_list) {
  lapply(data_list, head)
}

view_head(datasets)

# Função para verificar a estrutura de cada dataset
view_structure <- function(data_list) {
  lapply(data_list, str)
}

view_structure(datasets)

# Função para gerar resumo estatístico de cada dataset
view_summary <- function(data_list) {
  lapply(data_list, summary)
}

view_summary(datasets)

# Histograma para a variável quantidade
ggplot(datasets$ano_2024, aes(x = quantidade)) +
  geom_histogram(binwidth = 1, fill = "blue", color = "black") +
  labs(title = "Distribuição de Quantidade", x = "Quantidade", y = "Frequência")

# Gráfico de densidade para a variável preço
ggplot(datasets$ano_2024, aes(x = preco)) +
  geom_density(fill = "green", alpha = 0.5) +
  labs(title = "Densidade do Preço", x = "Preço", y = "Densidade")

identify_outliers <- function(data, variable) {
  if (!(variable %in% names(data))) {
    stop(paste("Variável", variable, "não encontrada no dataset."))
  }
  
  # Verificando se a coluna contém valores válidos
  if (all(is.na(data[[variable]]))) {
    stop(paste("Variável", variable, "está vazia ou contém apenas NA."))
  }
  
  lower_bound <- quantile(data[[variable]], 0.25, na.rm = TRUE) - 1.5 * IQR(data[[variable]], na.rm = TRUE)
  upper_bound <- quantile(data[[variable]], 0.75, na.rm = TRUE) + 1.5 * IQR(data[[variable]], na.rm = TRUE)
  
  data %>%
    filter(data[[variable]] < lower_bound | data[[variable]] > upper_bound)
}

# Aplicando a função com tryCatch e verificações adicionais
quantidade_outliers <- tryCatch({
  identify_outliers(datasets$ano_2024, "quantidade")
}, error = function(e) {
  message("Erro ao identificar outliers em 'quantidade': ", e)
  NULL
})

preco_outliers <- tryCatch({
  identify_outliers(datasets$ano_2024, "preco")
}, error = function(e) {
  message("Erro ao identificar outliers em 'preco': ", e)
  NULL
})

preco_outliers_sku <- tryCatch({
  identify_outliers(datasets$sku_price, "preco")
}, error = function(e) {
  message("Erro ao identificar outliers em 'preco' no dataset SKU: ", e)
  NULL
})

# Exibindo os outliers identificados (se houver)
list(quantidade_outliers, preco_outliers, preco_outliers_sku)

set.seed(123)
ano_2024_sample <- datasets$ano_2024 %>% sample_frac(sample_frac)

# Gráfico de dispersão entre quantidade e preço
ggplot(ano_2024_sample, aes(x = quantidade, y = preco)) +
  geom_point(alpha = 0.6) +
  labs(title = "Dispersão entre Quantidade e Preço", x = "Quantidade", y = "Preço")

# Gráfico de barras para quantidade vendida por loja
ggplot(ano_2024_sample, aes(x = cod_loja, y = quantidade)) +
  geom_bar(stat = "identity", fill = "blue") +
  labs(title = "Quantidade Vendida por Loja", x = "Código da Loja", y = "Quantidade") +
  theme(axis.text.x = element_text(angle = 90, hjust = 1))

# Cálculo da matriz de correlação para variáveis numéricas
numeric_vars <- ano_2024_sample %>%
  select_if(is.numeric) %>%
  na.omit()

cor_matrix <- cor(numeric_vars)
corrplot(cor_matrix, method = "color", type = "upper", tl.cex = 0.8, tl.col = "black", addCoef.col = "black")

# Realizando PCA nas variáveis numéricas
pca_result <- prcomp(numeric_vars, scale. = TRUE)

# Resumo dos componentes principais
summary(pca_result)

# Visualização das variâncias explicadas
fviz_eig(pca_result, addlabels = TRUE, ylim = c(0, 50))

# Visualização das variáveis no espaço dos componentes principais
fviz_pca_var(pca_result, 
             col.var = "contrib",
             gradient.cols = c("#00AFBB", "#E7B800", "#FC4E07"),
             repel = TRUE)

# Finalizar timer
end_time <- Sys.time()

# Mostre a quantidade de tempo que levou para executar o script e porcentagem do DataFrame amostrada
end_time - start_time
paste("Porcentagem do DataFrame amostrada:", sample_frac * 100, "%")
