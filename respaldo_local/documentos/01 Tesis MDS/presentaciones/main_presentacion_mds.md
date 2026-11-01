\documentclass[aspectratio=169]{beamer}
\usetheme{Madrid}
\usecolortheme{seagull}
\setbeamertemplate{navigation symbols}{}
\setbeamertemplate{footline}[frame number]

% ---- Paquetes ----
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{amsmath, amssymb, graphicx, booktabs, hyperref, xcolor}

% ---- Colores ----
\definecolor{myblue}{HTML}{0D47A1}
\setbeamercolor{background canvas}{bg=white}
\setbeamercolor{structure}{fg=myblue}
\setbeamercolor{frametitle}{fg=white,bg=myblue}
\definecolor{instblue}{HTML}{003B73}
\setbeamercolor{institute}{fg=instblue}
\setbeamerfont{institute}{size=\Large,series=\bfseries}

\setbeamercolor{headline}{bg=myblue}
\setbeamertemplate{headline}{%
  \begin{beamercolorbox}[wd=\paperwidth,ht=1.8ex,dp=0.4ex]{headline}%
  \end{beamercolorbox}%
}
\setbeamertemplate{frametitle}{%
  \nointerlineskip%
  \begin{beamercolorbox}[wd=\paperwidth,ht=2.6ex,dp=1.2ex,left]{frametitle}
    \hspace*{1ex}\insertframetitle
  \end{beamercolorbox}
}

% ---- Datos ----
\title[Avances Tesis]{Presentacion de Avances}
\subtitle{Deteccion \textbf{temporal} multimodal de emociones y atencion}
\author[Mario Romero]{Mario Romero}
\date{\today}

% NO \AtBeginSection para evitar diapositivas en blanco

\begin{document}

% ── Portada ──────────────────────────────────────────────────────
\begin{frame}
  \titlepage
\end{frame}

% ── Indice ───────────────────────────────────────────────────────
\begin{frame}{Contenidos}
\begin{columns}[t]
\column{0.5\textwidth}
\begin{enumerate}
  \item Contexto
  \item Oportunidades
  \item Hipotesis
  \item Preguntas de Investigacion
  \item Modelos propuestos
  \item Datos y senales
  \item Marco conceptual
\end{enumerate}
\column{0.5\textwidth}
\begin{enumerate}
  \setcounter{enumi}{7}
  \item Estado del Arte
  \item Evaluacion
  \item Preprocesamiento
  \item Siguientes pasos
  \item Roadmap
\end{enumerate}
\end{columns}
\end{frame}

% ===== 1. CONTEXTO =====
\section{Contexto}
\begin{frame}{Contexto}
\textbf{Tema:} Deteccion de emociones y nivel de interes con \emph{eye-tracking}, GSR, EEG y expresiones faciales en navegacion web.

\medskip
\textbf{Antecedente:} trabajos previos muestran buen desempeno por modalidad, pero con limitaciones al capturar la dinamica temporal.

\medskip
\textbf{Limitaciones actuales:}
\begin{itemize}
  \item Perdida de \textbf{dinamica temporal} (resumen por promedios/medianas).
  \item Fusion multimodal \textbf{tardia}, con mejoras potencialmente marginales.
\end{itemize}
\end{frame}

% ===== 2. OPORTUNIDADES =====
\section{Oportunidades}
\begin{frame}{Oportunidades}
\begin{block}{Idea central}
Modelo \textbf{multimodal temporal} que siga la evolucion de \emph{atencion} y \emph{emociones}.
\end{block}
\begin{itemize}
  \item Tratar atencion y emociones como \textbf{procesos dinamicos}.
  \item El aporte principal esta en la \textbf{temporalidad}, tipo de \textbf{fusion} y agregar variables.
\end{itemize}
\end{frame}

% ===== 3. HIPOTESIS =====
\section{Hipotesis}
\begin{frame}{Propuestas de Hipotesis}
\begin{block}{H1}
Los \textit{modelos temporales multimodales} superan a los modelos estaticos en la deteccion de \textbf{emociones} y \textbf{atencion}.
\end{block}
\begin{block}{H2}
Los \textit{modelos temporales multimodales} permiten capturar fenomenos de \textbf{fatiga} y \textbf{habituacion} durante la navegacion web.
\end{block}
\end{frame}

% ===== 4. PREGUNTAS =====
\section{Preguntas de Investigacion}
\begin{frame}{Preguntas de Investigacion}
\begin{enumerate}
  \item {?`}Cuanto aporta la \textbf{informacion temporal} frente a la informacion estatica?
  \item {?`}Que \textbf{arquitectura} (LSTM/GRU, TCN, Transformers) ofrece la mejor relacion desempeno-costo?
  \item {?`}Como influye el tipo de \textbf{fusion} (temprana/intermedia/tardia)?
  \item {?`}Se observan diferencias entre grupos demograficos (sexo y rango etario)?
  \item {?`}Que tipo de dato aporta mas a la deteccion de emociones y atencion?
\end{enumerate}
\end{frame}

% ===== 5. MODELOS =====
\section{Modelos propuestos}
\begin{frame}{Modelos propuestos}
\begin{columns}[t]
\column{0.5\textwidth}
\begin{itemize}
  \item \textbf{LSTM (o GRU)} multimodal
  \item \textbf{TCN} con dilataciones
\end{itemize}
\column{0.5\textwidth}
\begin{itemize}
  \item \textbf{Transformers} temporales
  \item \textbf{Baseline estatico}: MLP / SVM / Regresion Logistica
\end{itemize}
\end{columns}
\end{frame}

% ===== 6. SENALES =====
\section{Datos y senales}

% --- Pipeline general ---
\begin{frame}{Pipeline multimodal propuesto}
\begin{center}
\includegraphics[width=0.97\linewidth, height=0.82\textheight, keepaspectratio]{img_pipeline.png}
\end{center}
\end{frame}

% --- Modelos de emocion ---
\begin{frame}{Modelos de emocion: discreto vs. dimensional}
\begin{center}
\includegraphics[width=0.97\linewidth, height=0.82\textheight, keepaspectratio]{img_emociones.png}
\end{center}
\end{frame}

% --- Eye-tracking ---
\begin{frame}{Señal 1: Eye-Tracking}
\begin{center}
\includegraphics[width=0.97\linewidth, height=0.82\textheight, keepaspectratio]{img_eyetracking.png}
\end{center}
\end{frame}

% --- EEG ---
\begin{frame}{Señal 2: EEG — Electroencefalograma}
\begin{center}
\includegraphics[width=0.97\linewidth, height=0.82\textheight, keepaspectratio]{img_eeg.png}
\end{center}
\end{frame}

% --- GSR ---
\begin{frame}{Señal 3: GSR — Respuesta Galvanica}
\begin{center}
\includegraphics[width=0.97\linewidth, height=0.82\textheight, keepaspectratio]{img_gsr.png}
\end{center}
\end{frame}

% ===== 7. MARCO CONCEPTUAL =====
\section{Marco conceptual}
\begin{frame}{Marco conceptual}
\begin{enumerate}
  \item \textbf{Comportamiento del usuario como proceso dinamico}
  \begin{itemize}
    \item Emocion y atencion evolucionan en el tiempo.
    \item Una secuencia aporta mas informacion que frames aislados.
  \end{itemize}
  \item \textbf{Senales multimodales} --- capturan dimensiones complementarias del estado del usuario.
  \item \textbf{Fusion multimodal:} temprana / intermedia / tardia.
  \item \textbf{Modelamiento temporal:} captura habituacion, fatiga y transiciones de estado.
\end{enumerate}
\end{frame}

\begin{frame}{Estructura del Marco Teorico}
\begin{columns}[t]
\column{0.5\textwidth}
\begin{enumerate}
  \item HCI / comportamiento en entornos digitales
  \item Emociones humanas
  \item Atencion humana
  \item Expresiones (faciales y conductuales)
  \item Preprocesamiento de datos
  \item Analisis exploratorio (EDA)
  \item Modelamiento
\end{enumerate}
\column{0.5\textwidth}
\begin{enumerate}
  \setcounter{enumi}{7}
  \item Deteccion automatica de emociones
  \item Aprendizaje automatico clasico
  \item Aprendizaje profundo
  \item Transformers
  \item Transfer learning
  \item Evaluacion de modelos
  \item Estado del arte
\end{enumerate}
\end{columns}
\end{frame}

% ===================================================================
% ===== ESTADO DEL ARTE =============================================
% ===================================================================
\section{Estado del Arte}

% --- 1. Panorama y tendencias ---
\begin{frame}{Estado del Arte --- Panorama y tendencias}

\begin{itemize}\small
  \item Tendencia hacia \textbf{Transformers} y \textbf{fusion multimodal}
\end{itemize}

\vspace{0.3em}
{\scriptsize\textbf{Papers con Transformers + fusion multimodal:}}

\vspace{0.2em}
\scriptsize
\setlength{\tabcolsep}{3pt}
\renewcommand{\arraystretch}{1.05}

\tiny
\setlength{\tabcolsep}{5pt}
\renewcommand{\arraystretch}{1.20}
\begin{tabular}{llll}
\toprule
\textbf{Paper} & \textbf{Señales} & \textbf{Arquitectura} & \textbf{Aporte / Resultado} \\
\midrule
TACOformer (2023)   & EEG + GSR + ECG    & Cross-attn Transformer     & Atenc.\ token+canal; SOTA DEAP/Dreamer \\
Feng et al.\ (2025) & EEG + Facial       & Multi-head self-attn       & Fusion adaptativa EEG--Facial; 81.1\,\% (MED-HI) \\
Milmer (2025)       & EEG + Facial       & Swin Transf.\ + Cross-attn & MIL temporal sobre frames; 96.7\,\% (DEAP) \\
Wang et al.\ (2025) & EEG + Eye-tracking & Cross-modal attention      & Alineacion EEG--movimiento ocular; 90.6\,\% (SEED-IV) \\
MuMTAffect (2025)   & Gaze+Pupila+AU+GSR & Transf.\ por modalidad     & Encoders sep.; multitarea emocion--personalidad \\
GBV-Net (2025)      & EEG+GSR+ECG+Facial & Gated fusion jerarquica    & Fusion visio-fisiologica profunda \\
\bottomrule
\end{tabular}

\end{frame}


% --- 2. Emociones ---
\begin{frame}{Estado del Arte --- Emociones}

Dos grandes enfoques:
\begin{itemize}
  \item \textbf{Discreto} (Ekman): 6 emociones basicas.
  \item \textbf{Dimensional} (Russell): \emph{valencia--arousal}.

\end{itemize}

\begin{center}
\includegraphics[
  width=\linewidth,
  height=0.7\textheight,
  keepaspectratio
]{img_emociones.png}
\end{center}

\end{frame}

% --- 2. Resultados por modalidad ---


% --- 3. Fusion multimodal ---
\begin{frame}{Estado del Arte --- Estrategias de fusion multimodal}
\begin{center}
\includegraphics[width=0.96\linewidth, height=0.56\textheight, keepaspectratio]{img_fusion.png}
\end{center}
\begin{alertblock}{Importancia:}
\small La ganancia multimodal depende de la \textbf{arquitectura de fusion}, no solo de agregar modalidades.
{\scriptsize Zali-Vargahan et al.\ (2023): 95.3\,\% con fusion CNN+Stockwell (EEG+fisio+facial).
Saavedra (2024): sin mejora significativa con fusion tardia EEG+GSR en contexto web.}
\end{alertblock}
\end{frame}

% --- 4. Modelamiento temporal ---
\begin{frame}{Estado del Arte --- Modelamiento temporal}
\begin{center}
\includegraphics[width=0.96\linewidth, height=0.54\textheight, keepaspectratio]{img_modelos.png}
\end{center}
\begin{block}{Referencias clave por arquitectura}
\scriptsize
\textbf{LSTM:} Saffie (2023) --- EEG web. \quad
\textbf{TCN:} Bai et al.\ (2018); Kamrud et al.\ (2021) --- EEG; Elmadjian et al.\ (2022) --- eye-tracking. \quad
\textbf{Transformer:} Vaswani et al.\ (2017); MNT (2022) --- EEG+PPG+GSR; TEREE (2025) --- EEG+eye-tracking.
\end{block}
\end{frame}

% --- 5. Brechas y aporte ---
\begin{frame}{Estado del Arte --- Brechas y aporte de esta tesis}
\begin{columns}[t]
\column{0.52\textwidth}
\textbf{Brechas en la literatura}
\begin{enumerate}\small
  \item Senales tratadas como \textbf{vectores estaticos}, sin dinamica temporal
   
  \item Fusion de \textbf{4 señales} en contexto web: inexistente
   
  \item \textbf{Fatiga y habituacion} no modeladas como variable de interes

  \item Sin \textbf{ablation studies} sistematicos

\end{enumerate}
\column{0.44\textwidth}
\textbf{Aporte de esta tesis}
\begin{itemize}\small
  \item[\textcolor{myblue}{\checkmark}] Modelos secuenciales \textbf{EEG+GSR+Eye+Facial}.
  \item[\textcolor{myblue}{\checkmark}] Comparacion \textbf{early / intermediate / late fusion}.
  \item[\textcolor{myblue}{\checkmark}] Deteccion de \textbf{fatiga y habituacion} (H2).
  \item[\textcolor{myblue}{\checkmark}] \textbf{Ablation study} por modalidad y temporalidad.
  \item[\textcolor{myblue}{\checkmark}] Baseline estatico como control.
\end{itemize}
\end{columns}
\end{frame}

% ===================================================================

% ===== 8. EVALUACION =====
\section{Evaluacion}
\begin{frame}{Estrategia de evaluacion}
\begin{itemize}
  \item Metricas por ventana temporal: F1-score, AUC.
  \item Comparacion contra \textbf{baseline estatico}.
  \item \textbf{Ablation study}: que parte aporta mas valor
  \begin{itemize}
    \item Sin temporalidad (features agregadas).
    \item Sin una modalidad (solo eye-tracking / solo facial / solo GSR / solo EEG).
    \item Sin fusion (ensembles tardios).
  \end{itemize}
  \item Medicion de costo: latencia de inferencia y complejidad del modelo.
\end{itemize}
\end{frame}

\begin{frame}{Resumen del aporte}
\begin{itemize}
  \item Extiende trabajos previos incorporando \textbf{dinamica temporal}.
  \item Propone un enfoque \textbf{multimodal y secuencial}.
  \item Fortalece la evaluacion mediante \textbf{baselines} y \textbf{ablations}.
\end{itemize}
\end{frame}

% ===== PREPROCESAMIENTO =====
\section{Preprocesamiento}

\begin{frame}{Pre procesamiento}
\begin{itemize}
    \item Videos de toma de muestra 2.
    \item Armando dataframe de Eye-tracking para realizar EDA.
\end{itemize}
\end{frame}

\begin{frame}{Avance 1: preprocesamiento de eye-tracking}
\textbf{Estado actual:} Construyendo el \textbf{dataframe base de eye-tracking} y el pipeline de limpieza.
\medskip
\begin{itemize}
    \item Revision de los \textbf{videos y registros de toma de muestra 2}.
    \item Identificacion de la \textbf{estructura de los datos crudos}.
    \item Construccion inicial de un \textbf{dataframe unificado} para EDA.
    \item Variables relevantes para modelamiento temporal:
    \begin{itemize}
        \item fijaciones, sacadas, duracion de eventos
        \item coordenadas de mirada, diametro pupilar
    \end{itemize}
\end{itemize}
\end{frame}

\begin{frame}{Avance 2: definicion inicial de features}
\begin{columns}[t]
\column{0.5\textwidth}
\textbf{Eye-tracking}
\begin{itemize}
  \item Numero de fijaciones
  \item Duracion promedio de fijaciones
  \item Amplitud y velocidad de sacadas
  \item Dispersion de la mirada
  \item Diametro pupilar promedio
\end{itemize}
\textbf{GSR}
\begin{itemize}
  \item Numero de picos (SCR)
  \item Amplitud de respuesta
  \item Nivel tonico (SCL)
  \item Variabilidad de la senal
\end{itemize}
\column{0.5\textwidth}
\textbf{EEG}
\begin{itemize}
  \item Potencia por bandas (delta, theta, alpha, beta, gamma)
  \item Relaciones entre bandas
\end{itemize}
\textbf{Expresion facial}
\begin{itemize}
  \item Embeddings faciales
  \item Probabilidades de emocion (FaceReader)
\end{itemize}
\end{columns}
\end{frame}

% ===== SIGUIENTES PASOS =====
\section{Siguientes pasos}
\begin{frame}{Siguientes pasos}
\begin{itemize}
  \item Completar el \textbf{preprocesamiento} y sincronizacion temporal de senales.
  \item Construir \textbf{caracteristicas por modalidad} desde un baseline:
  \begin{itemize}
    \item faciales, oculares, GSR, EEG
  \end{itemize}
  \item Probar \textbf{predicciones unimodales} para cada modalidad por separado.
  \item Evaluar \textbf{predicciones multimodales} con distintas combinaciones.
  \item Analizar el aporte incremental de cada modalidad respecto del \textbf{baseline}.
\end{itemize}
\end{frame}

% ===== ROADMAP =====
\section{Roadmap}
\begin{frame}{Roadmap de trabajo 2026}
\small
\begin{table}
\centering
\begin{tabular}{p{2.3cm} p{8.2cm}}
\toprule
\textbf{Periodo} & \textbf{Objetivo principal} \\
\midrule
Abril      & Completar preprocesamiento, limpieza y sincronizacion temporal \\
Mayo       & EDA y baselines iniciales \\
Junio      & Modelos temporales (LSTM / GRU / TCN) \\
Julio      & Fusion multimodal \\
Agosto     & Evaluacion completa, metricas y ablation study \\
Septiembre & Analisis de resultados y conclusiones preliminares \\
Octubre    & Redaccion de capitulos principales \\
Noviembre  & Correcciones e integracion final \\
Diciembre  & Preparacion de defensa \\
\bottomrule
\end{tabular}
\end{table}
\medskip
\textbf{Hito actual:} cierre del preprocesamiento de eye-tracking y definicion de features.
\end{frame}

\begin{frame}{}
\centering
\vspace{1cm}
{\Large \textbf{Gracias}}\\[1em]
{?`}Preguntas?
\end{frame}

\end{document}