// Boyer-Myrvold is only a witness proposer. Python independently verifies
// every nonplanarity certificate as a K5/K3,3 subdivision before adding a cut.
#include <boost/graph/adjacency_list.hpp>
#include <boost/graph/boyer_myrvold_planar_test.hpp>
#include <iostream>
#include <vector>
using namespace boost;
using G=adjacency_list<vecS,vecS,undirectedS,no_property,property<edge_index_t,int>>;
int main(){std::ios::sync_with_stdio(false);std::cin.tie(nullptr);
 int n,m;while(std::cin>>n>>m){if(n<1||n>1000||m<0||m>100000)return 2;G g(n);
 for(int i=0,a,b;i<m;i++){if(!(std::cin>>a>>b)||a<0||a>=n||b<0||b>=n||a==b)return 3;auto e=add_edge(a,b,g).first;put(edge_index,g,e,i);}
 std::vector<graph_traits<G>::edge_descriptor>w;
 bool good=boyer_myrvold_planarity_test(boyer_myrvold_params::graph=g,boyer_myrvold_params::kuratowski_subgraph=std::back_inserter(w));
 if(good)std::cout<<"P\n";
 else{std::cout<<"C "<<w.size();for(auto e:w)std::cout<<" "<<source(e,g)<<" "<<target(e,g);std::cout<<"\n";}std::cout.flush();
 }return 0;}
