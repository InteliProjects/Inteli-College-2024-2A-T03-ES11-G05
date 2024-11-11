import { RecentSearches } from '../../components/recentSearches';
import { PopularProducts } from '../../components/popularProducts';
import { NavBar } from '../../components/navBar';
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { ProductsListed } from './productsListed';


export function SalesMan() {
  return (
    <div className="max-w-lg mx-auto p-4">
      <div className="max-w-lg mx-auto">
        <NavBar userRoute="/dash" salesManRoute="/salesMan" isManagerPage={false}/>
      </div>

      <Tabs className='bg-white' defaultValue="All">
        <TabsList className='bg-white'>
          <TabsTrigger className='data-[state=active]:text-[#DD5D79] data-[state=active]:underline bg-white rounded-none !shadow-none' value="All">All</TabsTrigger>
          <TabsTrigger className='data-[state=active]:text-[#DD5D79] data-[state=active]:underline bg-white rounded-none !shadow-none' value="Perfume">Perfume</TabsTrigger>
          <TabsTrigger className='data-[state=active]:text-[#DD5D79] data-[state=active]:underline bg-white rounded-none !shadow-none' value="Makeup">Makeup</TabsTrigger>
          <TabsTrigger className='data-[state=active]:text-[#DD5D79] data-[state=active]:underline bg-white rounded-none !shadow-none' value="Cabelos">Cabelos</TabsTrigger>
          <TabsTrigger className='data-[state=active]:text-[#DD5D79] data-[state=active]:underline bg-white rounded-none !shadow-none' value="Unhas">Unhas</TabsTrigger>
        </TabsList>
        <TabsContent value="All">
          <RecentSearches />
          <PopularProducts />
        </TabsContent>
        <TabsContent value="Perfume">
          <ProductsListed/>
        </TabsContent>
      </Tabs>

    </div>
  );
}
