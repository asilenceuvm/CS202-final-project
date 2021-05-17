
  .globl add
add:
  pushq %rbp
  movq %rsp, %rbp
  subq $0, %rsp
  pushq %rbx
  pushq %r12
  pushq %r13
  pushq %r14


  jmp add_start
add_start:
  movq %rdi, %rdx
  movq %rsi, %rcx
  movq %rdx, %rdx
  addq %rcx, %rdx
  movq %rdx, %rax
  jmp add_conclusion
add_conclusion:

  addq $0, %rsp
  subq $0, %r15
  popq %r14
  popq %r13
  popq %r12
  popq %rbx
  popq %rbp
  retq

  .globl main
main:
  pushq %rbp
  movq %rsp, %rbp
  subq $0, %rsp
  pushq %rbx
  pushq %r12
  pushq %r13
  pushq %r14

  movq $16384, %rdi
  movq $16, %rsi
  callq initialize
  movq rootstack_begin(%rip), %r15

  jmp main_start
label_960:
  movq free_ptr(%rip), %rdx
  addq $16, free_ptr(%rip)
  movq %rdx, %r11
  movq $3, 0(%r11)
  movq %rdx, %r11
  movq %rbx, 8(%r11)
  movq $0, %rcx
  movq %rdx, %rdx
  movq %rdx, %r11
  movq 8(%r11), %rdx
  movq $5, %rdi
  movq $6, %rsi
  movq %rdx, %rax
  callq *%rax
  jmp main_conclusion
label_961:
  movq $0, %rdx
  jmp label_960
label_962:
  movq %r15, %rdi
  movq $16, %rsi
  callq collect
  jmp label_960
main_start:
  leaq add(%rip), %rbx
  movq free_ptr(%rip), %rdx
  movq %rdx, %rdx
  addq $16, %rdx
  movq fromspace_end(%rip), %rcx
  cmpq %rcx, %rdx
  jl label_961
  jmp label_962
main_conclusion:

  movq %rax, %rdi
  callq print_int
  movq $0, %rax

  addq $0, %rsp
  subq $0, %r15
  popq %r14
  popq %r13
  popq %r12
  popq %rbx
  popq %rbp
  retq
