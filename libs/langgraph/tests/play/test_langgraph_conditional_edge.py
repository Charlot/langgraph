import time
from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Any
import copy
from IPython.display import display, Image

from dotenv import load_dotenv

load_dotenv()

class State(TypedDict):
    hello_a: str
    hello_b: str
    hello_c: str
    hello_d: str
    hello_e: str
    hello_f: str
    hello_g: str
    hello_h: str
    hello_i: str
    hello_j: str
    hello_k: str
    hello_l: str
    hello_m: str
    hello_n: str


def node_a(state: State) -> State:
    print("node_a")
    return {"hello_a": "hello_a"}

def route_fun_a_multi_nodes(state: State)->Any:
    print("route_fun_a_multi_nodes")
    return "1","2"

def route_fun_a_branch(state: State)->Any:
    print("route_fun_a_branch")
    return 1

def node_b(state: State) -> State:
    print("node_b")
    return {"hello_b": "hello_b"}

def node_c(state: State) -> State:
    print("node_c")
    return {"hello_c": "hello_c"}

def node_d(state: State) -> State:
    print("node_d")
    return {"hello_d": "hello_d"}

def node_e(state: State) -> State:
    print("node_e")
    return {"hello_e": "hello_e"}

def node_f(state: State) -> State:
    print("node_f")
    time.sleep(5)
    return {"hello_f": "hello_f"}

def node_g(state: State) -> State:
    print("node_g")
    return {"hello_g": "hello_g"}

def node_h(state: State) -> State:
    print("node_h")
    return {"hello_h": "hello_h"}

def node_i(state: State) -> State:
    print("node_i")
    return {"hello_i": "hello_i"}

def node_j(state: State) -> State:
    print("node_j")
    return {"hello_j": "hello_j"}

def node_k(state: State) -> State:
    print("node_k")
    return {"hello_k": "hello_k"}

def node_l(state: State) -> State:
    print("node_l")
    return {"hello_l": "hello_l"}

def node_m(state: State) -> State:
    print("node_m")
    return {"hello_m": "hello_m"}

def node_n(state: State) -> State:
    print("node_n")
    return {"hello_n": "hello_n"}

def route_fun_a_2(state: State)->bool:
    print("route_fun_a_2")
    return 2

def test_conditional_edge() -> None:
    builder=StateGraph(State)
    builder.add_node("a",node_a)
    builder.add_node("b",node_b)
    builder.add_node("c",node_c)
    builder.add_node("d",node_d)
    builder.add_node("e",node_e)
    builder.set_entry_point("a")

    builder.add_conditional_edges("a", path=route_fun_a_multi_nodes,path_map={"1":"b","2":"c","3":"e"})
    
    builder.add_edge("b","d")
    builder.add_edge("c","d")
    builder.add_edge("a","e")
    builder.add_edge("e","d")
    
    graph = builder.compile()
    
    print(graph.get_graph().draw_ascii())


    graph.invoke(input={})


def test_conditional_edge_branch_merge() -> None:
    """简单merge测试
            
    """
    builder=StateGraph(State)
    builder.add_node("a",node_a)
    builder.add_node("b",node_b)
    builder.add_node("c",node_c)
    builder.add_node("d",node_d)
    builder.add_node("e",node_e)
    

    builder.add_edge(START, "a")
    builder.add_node("branch1", lambda x:{})
    builder.add_conditional_edges("a", path=route_fun_a_branch,path_map={0:"branch",1:"d"})
    builder.add_edge("branch", "b")
    builder.add_edge("branch", "c")
    builder.add_edge("b", "e")
    builder.add_edge("c", "e")
    builder.add_edge("d", "e")
    builder.add_edge("e", END)
    
    graph = builder.compile()
    
    print(graph.get_graph().draw_ascii())


    graph.invoke(input={})

    #
    #     +-----------+        
    #     | __start__ |        
    #     +-----------+        
    #             *             
    #             *             
    #             *             
    #         +---+            
    #         | a |            
    #         +---+..          
    #         .      ..        
    #         .         ..      
    #         .            ..    
    # +--------+            .   
    # | branch |            .   
    # +--------+            .   
    #     *    *             .   
    #     *      *            .   
    # *        *           .   
    # +---+     +---+      +---+  
    # | b |*    | c |      | d |  
    # +---+ *   +---+     *+---+  
    #     ***   *    **        
    #         *   * **          
    #         ** **            
    #         +---+            
    #         | e |            
    #         +---+            
    #             *             
    #             *             
    #             *             
    #         +---------+         
    #         | __end__ |         
    #         +---------+ 



def test_conditional_edge_branch_fork() -> None:
    """简单merge测试-waiting
            
    """
    builder=StateGraph(State)
    builder.add_node("a",node_a)
    builder.add_node("b",node_b)
    builder.add_node("c",node_c)
    builder.add_node("d",node_d)
    builder.add_node("e",node_e)
    builder.add_node("f",node_f)
    builder.add_node("g",node_g)

    builder.add_edge(START, "a")
    builder.add_node("branch", lambda x:{})
    builder.add_conditional_edges("a", path=route_fun_a_branch,path_map={0:"branch",1:"d"})
    builder.add_edge("branch", "b")
    builder.add_edge("branch", "c")
    builder.add_edge("b", "e")
    builder.add_edge("c", "e")
    builder.add_edge("d", "f")
    builder.add_edge(("d","g"), "e") # 如果不是waitting，e会执行2次
    builder.add_edge("f", "g")
    builder.add_edge("e", END)
    
    graph = builder.compile()
    
    print(graph.get_graph().draw_ascii())


    graph.invoke(input={})

    """
       +-----------+              
           | __start__ |              
           +-----------+              
                  *                   
                  *                   
                  *                   
               +---+                  
               | a |.                 
              .+---+ .                
            ..        ...             
          ..             .            
         .                ...         
     +---+                   .        
     | d |                   .        
     +---+                   .        
     *    *                  .        
    *     *                  .        
   *       *                 .        
+---+       *           +--------+    
| f |       *           | branch |    
+---+       *           +--------+    
  *         *             *     *     
  *         *             *     *     
  *         *            *       *    
+---+       *        +---+     +---+  
| g |*       *       | b |     | c |  
+---+ ***     *      +---+  ***+---+  
         ***   *     *   ***          
            *** *   * ***             
               *** ***                
               +---+                  
               | e |                  
               +---+                  
                  *                   
                  *                   
                  *                   
            +---------+               
            | __end__ |               
            +---------+        
    """



def test_conditional_edge_branch_multi_branchs() -> None:
    """简单merge测试-waiting 多个branch
            
    """
    builder=StateGraph(State)
    builder.add_node("a",node_a)
    builder.add_node("b",node_b)
    builder.add_node("c",node_c)
    builder.add_node("d",node_d)
    builder.add_node("e",node_e)
    builder.add_node("f",node_f)
    builder.add_node("g",node_g)
    builder.add_node("h",node_h,defer=True) # 解决多变等待问题
    builder.add_node("i",node_i)
    builder.add_node("j",node_j)
    builder.add_node("k",node_k)
    builder.add_node("l",node_l,defer=True) # 解决多变等待问题，但是如果来自条件边的节点连接了l，其它边使用.虚线的方式连接了

    builder.add_edge(START, "a")
    builder.add_edge("a", "i")

    builder.add_node("branch1", lambda x:x)
    builder.add_node("branch2", lambda x:x)

    builder.add_conditional_edges("a", path=route_fun_a_branch,path_map={0:"branch1",1:"branch2"})
    builder.add_edge("branch1", "b")
    builder.add_edge("branch1", "c")
    builder.add_edge("branch1", "k")

    builder.add_edge("branch2", "d")
    builder.add_edge("branch2", "e")

    builder.add_edge("b","j")
    builder.add_edge("j","h")
    builder.add_edge("c","l")
    builder.add_edge("i","l")
    # builder.add_edge("k","l")
    # builder.add_edge("g","l")



    builder.add_edge("d","f")
    builder.add_edge("e","g")
    builder.add_edge("f","h")
    builder.add_edge("g","h")

    builder.add_edge("i", "h") # 由于i的存在，h会执行2次
    builder.add_edge("h", END)

    graph = builder.compile()
    
    print(graph.get_graph().draw_ascii())
    print(graph.get_graph().draw_mermaid(with_styles=False))
    


    graph.invoke(input={})

    """
                          +-----------+                       
                      | __start__ |                       
                      +-----------+                       
                             *                            
                             *                            
                             *                            
                          +---+                           
                         .| a |..                         
                      ... +---+  ...                      
                 .....    *         ...                   
              ...         *            ...                
           ...           *                ..              
  +---------+           *               +---------+       
  | branch2 |           *               | branch1 |       
  +---------+           *               +---------+       
     *    *             *              ***   *    *       
    *      *            *             *     *      *      
   *        *           *           **      *       **    
+---+     +---+         *       +---+       *         *   
| d |     | e |         *       | b |       *         *   
+---+     +---+         *       +---+       *         *   
  *         *           *         *         *         *   
  *         *           *         *         *         *   
  *         *           *         *         *         *   
+---+.    +---+       +---+     +---+     +---+       *   
| f |*....| g |.      | i |    *| j |    *| c |       *   
+---+ *** +---+*...   +---+ *** +---+ *** +---+       *   
         **** ..*. ..*.   **   .    **                *   
             *** *...* *** *   . ***                  *   
                *** ***.....* .**                     *   
                +---+     +---+                    *+---+ 
                | h |*    | l |                **** | k | 
                +---+ **  +---+            ****     +---+ 
                        *    *         ****               
                         **  *     ****                   
                           * *   **                       
                        +---------+                       
                        | __end__ |                       
                        +---------+   
    """

def test_conditional_edge_defer() -> None:
    """defer测试
    """
    builder=StateGraph(State)
    builder.add_node("a",node_a)
    builder.add_node("b",node_b,defer=True) # b加上defer会让d/f执行2次
    builder.add_node("c",node_c)
    builder.add_node("d",node_d)
    builder.add_node("e",node_e)
    builder.add_node("f",node_f,defer=True) # f加上defer可以只执行一次，但是不能b也加

    builder.set_entry_point("a")
    builder.add_edge("a", "b")
    builder.add_edge("a", "c")
    builder.add_conditional_edges("b",lambda x:1, {1:"d", 0:"e"})
    builder.add_conditional_edges("c", lambda x:1, {1:"d", 0:"e"})
    builder.add_edge("c", "d")
    builder.add_edge("d", "f")
    builder.add_edge("e", "f")
    builder.add_edge("a", "f")

    graph = builder.compile()
    print(graph.get_graph().draw_ascii())
    # print(graph.get_graph().draw_mermaid(with_styles=False))
    graph.invoke(input={})


if __name__ == "__main__":
    # test_conditional_edge()
    # test_conditional_edge_branch_merge()
    # test_conditional_edge_branch_fork()
    # test_conditional_edge_branch_multi_branchs()
    test_conditional_edge_defer()



