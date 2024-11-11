import { useRef, useState } from 'react';
import { Input } from "@/components/ui/input";
import { Eye, EyeOff } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { motion } from 'framer-motion';
import { login } from '@/api/login';
import { useNavigate } from 'react-router-dom';
import { useToast } from '@/hooks/use-toast';
import { useUserStore } from '@/zustand/user';

export function Login() {
    const navigate = useNavigate()
    // Estado para controlar a visibilidade da senha
    const [showPassword, setShowPassword] = useState(false);
    const setUser = useUserStore((state) => state.setUser)

    // Função para alternar entre mostrar e ocultar a senha
    const togglePasswordVisibility = () => {
        setShowPassword(!showPassword);
    };

    // Variantes de animação para os elementos
    const containerVariants = {
        hidden: { opacity: 0, y: 50 },
        visible: { opacity: 1, y: 0, transition: { duration: 0.8, ease: 'easeOut' } }
    };

    const { toast } = useToast()

    const emailRef = useRef<HTMLInputElement>(null)
    const passwordRef = useRef<HTMLInputElement>(null)

    const handleButtonClick = async () => {

        if (emailRef.current && passwordRef.current) {
            const email = emailRef.current.value
            const password = passwordRef.current.value

            const result:{
                access_token: string;
                token_type: string;
                user: {
                  id: string;
                  email: string;
                  role: string;
                };
              } = await login(email, password)

            if (result) {
                setUser({email:result.user.email, access_toke:result.access_token})

                if(result.user.email === "gerente@cosmeticoders.com.br"){
                    navigate('/manager')
                }else{
                    navigate("/salesMan")
                }


                toast({
                    className: 'bg-green-500 border-0 text-white',
                    title: 'Login realizado com suceso',
                    description: `Seja bem vindo ${result.user.email}`,
                })
            } else {
                toast({
                    className: 'bg-red-500 border-0 text-white',
                    title: 'Failed login :(',
                    description: 'Demo Vault !!',
                })
            }
        } else {
            // TODO: Toast com erro e validações nos inputs
            console.error('Os campos de email e senha não podem estar vazios.')
        }
    }

    return (
        <motion.div
            className="p-5 mt-16"
            initial="hidden"
            animate="visible"
            variants={containerVariants}
        >
            <motion.div className="w-48 mb-24">
                <motion.h1
                    className="text-[30px] font-bold leading-[130%] tracking-[-0.3px] text-[#1E232C] font-poppins"
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 1, delay: 0.2 }}
                >
                    Bem vindo ao ComesticCo Assistent.
                </motion.h1>
            </motion.div>

            <motion.div
                className="flex flex-col gap-3 mb-14"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.8, delay: 0.5 }}
            >
                {/* Input para o Email */}
                <Input ref={emailRef} className="border border-[#E8ECF4] h-14 bg-[#F7F8F9] text-lg" placeholder="Email" />

                {/* Campo de Senha */}
                <div className="relative">
                    <Input
                        ref={passwordRef}
                        type={showPassword ? "text" : "password"} // Alterna entre password e text
                        className="border border-[#E8ECF4] h-14 bg-[#F7F8F9] pr-10 text-lg" // Adiciona padding-right para o ícone
                        placeholder="Senha"
                    />
                    {/* Botão para mostrar/ocultar senha */}
                    <button
                        type="button"
                        onClick={togglePasswordVisibility}
                        className="absolute inset-y-0 right-3 flex items-center"
                    >
                        {showPassword ? (
                            <Eye className="w-5 h-5 text-gray-600" />
                        ) : (
                            <EyeOff className="w-5 h-5 text-gray-600" />
                        )}
                    </button>
                </div>
            </motion.div>

            <motion.div
                className="mt-5"
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.6, delay: 0.7 }}
            >
                <Button onClick={handleButtonClick} className='bg-[#DD5D79] rounded-lg h-12 w-full text-lg'>Login</Button>
            </motion.div>
        </motion.div>
    );
}
