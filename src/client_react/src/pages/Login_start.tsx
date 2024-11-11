import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";

export function Login_start() {
    // Animações para os elementos principais
    const textAnimation = {
        hidden: { opacity: 0, y: 50 },
        visible: { opacity: 1, y: 0, transition: { duration: 1 } },
    };

    const buttonAnimation = {
        hidden: { opacity: 0, scale: 0.8 },
        visible: { opacity: 1, scale: 1, transition: { delay: 1, duration: 0.5 } },
    };

    const backgroundAnimation = {
        hidden: { opacity: 0 },
        visible: { opacity: 1, transition: { delay: 0.5, duration: 1 } },
    };

    const navigate = useNavigate()

    return (
        <div className="flex flex-col items-center justify-center h-screen bg-white">
            {/* Background shapes */}
            <motion.div
                className="absolute top-0 left-0 w-full h-full"
                variants={backgroundAnimation}
                initial="hidden"
                animate="visible"
            >
                {/* Círculos e outros elementos */}
                <motion.div
                    className="w-80 h-80 bg-[#FFCBCB] rounded-full absolute -top-16 left-48"
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ delay: 0.3, duration: 1 }}
                />
                <motion.div
                    className="w-56 h-56 border-4 border-[#FFCBCB] rounded-full absolute -top-10 -left-5"
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ delay: 0.6, duration: 1 }}
                />
                <motion.div
                    className="w-20 h-20 border-2 border-[#FFCBCB] rounded-full absolute top-16 left-14"
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ delay: 0.9, duration: 1 }}
                />
            </motion.div>

            {/* SVGs animados */}
            <motion.div className="absolute top-64 left-32" variants={backgroundAnimation} initial="hidden" animate="visible">
                <svg xmlns="http://www.w3.org/2000/svg" width="106" height="55" viewBox="0 0 106 55" fill="none">
                    <mask id="path-1-inside-1_193_120" fill="white">
                        <path fill-rule="evenodd" clip-rule="evenodd" d="M0.0352397 0C0.0118139 0.647405 0 1.29777 0 1.9509C0 31.222 23.7289 54.9509 53 54.9509C82.2711 54.9509 106 31.222 106 1.9509C106 1.29777 105.988 0.647405 105.965 0H0.0352397Z" />
                    </mask>
                    <path fill-rule="evenodd" clip-rule="evenodd" d="M0.0352397 0C0.0118139 0.647405 0 1.29777 0 1.9509C0 31.222 23.7289 54.9509 53 54.9509C82.2711 54.9509 106 31.222 106 1.9509C106 1.29777 105.988 0.647405 105.965 0H0.0352397Z" fill="white" />
                    <path d="M0.0352397 0V-1H-0.929231L-0.964106 -0.0361605L0.0352397 0ZM105.965 0L106.964 -0.036155L106.929 -1H105.965V0ZM1 1.9509C1 1.30983 1.0116 0.671521 1.03459 0.0361605L-0.964106 -0.0361605C-0.987968 0.62329 -1 1.28571 -1 1.9509H1ZM53 53.9509C24.2812 53.9509 1 30.6697 1 1.9509H-1C-1 31.7743 23.1766 55.9509 53 55.9509V53.9509ZM105 1.9509C105 30.6697 81.7188 53.9509 53 53.9509V55.9509C82.8234 55.9509 107 31.7743 107 1.9509H105ZM104.965 0.036155C104.988 0.671523 105 1.30984 105 1.9509H107C107 1.28571 106.988 0.623288 106.964 -0.036155L104.965 0.036155ZM105.965 -1H0.0352397V1H105.965V-1Z" fill="#FFCBCB" mask="url(#path-1-inside-1_193_120)" />
                </svg>
            </motion.div>

            <motion.div className="absolute top-80 left-16" variants={backgroundAnimation} initial="hidden" animate="visible">
                <svg xmlns="http://www.w3.org/2000/svg" width="159" height="136" viewBox="0 0 159 136" fill="none">
                    <mask id="path-1-inside-1_193_123" fill="white">
                        <path fill-rule="evenodd" clip-rule="evenodd" d="M16.4475 0.0316974C15.834 0.881133 15.2335 1.74499 14.6463 2.62318C-11.668 41.9804 -1.09466 95.2176 38.2625 121.532C77.6197 147.846 130.857 137.273 157.171 97.9157C157.758 97.0375 158.327 96.1524 158.878 95.2609L16.4475 0.0316974Z" />
                    </mask>
                    <path fill-rule="evenodd" clip-rule="evenodd" d="M16.4475 0.0316974C15.834 0.881133 15.2335 1.74499 14.6463 2.62318C-11.668 41.9804 -1.09466 95.2176 38.2625 121.532C77.6197 147.846 130.857 137.273 157.171 97.9157C157.758 97.0375 158.327 96.1524 158.878 95.2609L16.4475 0.0316974Z" fill="white" />
                    <path d="M16.4475 0.0316974L17.0034 -0.799609L16.2016 -1.33568L15.6369 -0.553814L16.4475 0.0316974ZM158.878 95.2609L159.729 95.7863L160.235 94.9656L159.434 94.4296L158.878 95.2609ZM15.4776 3.17899C16.0581 2.31083 16.6517 1.45687 17.2582 0.617208L15.6369 -0.553814C15.0163 0.305393 14.4089 1.17915 13.815 2.06736L15.4776 3.17899ZM38.8183 120.701C-0.0797271 94.6933 -10.5297 42.0771 15.4776 3.17899L13.815 2.06736C-12.8063 41.8837 -2.10959 95.742 37.7067 122.363L38.8183 120.701ZM156.34 97.3599C130.333 136.258 77.7164 146.708 38.8183 120.701L37.7067 122.363C77.523 148.985 131.381 138.288 158.003 98.4715L156.34 97.3599ZM158.027 94.7355C157.483 95.6168 156.92 96.4917 156.34 97.3599L158.003 98.4715C158.596 97.5833 159.172 96.6881 159.729 95.7863L158.027 94.7355ZM159.434 94.4296L17.0034 -0.799609L15.8917 0.863004L158.322 96.0922L159.434 94.4296Z" fill="#FFCBCB" mask="url(#path-1-inside-1_193_123)" />
                </svg>
            </motion.div>

            {/* Conteúdo principal */}
            <motion.div
                className="relative z-10 flex items-end text-center h-screen mb-16 p-5"
                variants={textAnimation}
                initial="hidden"
                animate="visible"
            >
                <div className="text-start ">
                    <motion.h1 className="text-4xl font-bold text-gray-800 mb-4" variants={textAnimation}>
                        ComesticCo Assistente.
                    </motion.h1>
                    <motion.p className="text-black mb-14 w-72" variants={textAnimation}>
                        Sua assistente para recomendação de produtos e controle dos seus ganhos.
                    </motion.p>
                    <motion.div className="flex justify-center" variants={buttonAnimation}>
                        <button onClick={()=> navigate("/login")} className="bg-[#DD5D79] text-white font-semibold py-3 px-6 rounded-lg shadow-lg">
                            Comece Agora
                        </button>
                    </motion.div>
                </div>
            </motion.div>
        </div>
    );
}
