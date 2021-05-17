
  .globl addToVec
addToVec:
  pushq %rbp
  movq %rsp, %rbp
  subq $0, %rsp
  pushq %rbx
  pushq %r12
  pushq %r13
  pushq %r14

  movq $0, (%r15)
  addq $8, %r15

  jmp addToVec_start
label_981:
  movq free_ptr(%rip), %rdx
  addq $16, free_ptr(%rip)
  movq %rdx, %r11
  movq $131, 0(%r11)
  movq %rdx, %r11
  movq -8(%r15), %rax
  movq %rax, 8(%r11)
  movq $0, %rcx
  movq %rdx, %rdx
  movq %rdx, %rax
  jmp addToVec_conclusion
label_982:
  movq $0, %rdx
  jmp label_981
label_983:
  movq %r15, %rdi
  movq $16, %rsi
  callq collect
  jmp label_981
label_984:
  movq free_ptr(%rip), %rdx
  addq $16, free_ptr(%rip)
  movq %rdx, %r11
  movq $3, 0(%r11)
  movq %rdx, %r11
  movq %rbx, 8(%r11)
  movq $0, %rcx
  movq %rdx, -8(%r15)
  movq free_ptr(%rip), %rdx
  movq %rdx, %rcx
  addq $16, %rcx
  movq fromspace_end(%rip), %rdx
  cmpq %rdx, %rcx
  jl label_982
  jmp label_983
label_985:
  movq $0, %rdx
  jmp label_984
label_986:
  movq %r15, %rdi
  movq $16, %rsi
  callq collect
  jmp label_984
addToVec_start:
  movq $42, %rbx
  movq free_ptr(%rip), %rdx
  movq %rdx, %rdx
  addq $16, %rdx
  movq fromspace_end(%rip), %rcx
  cmpq %rcx, %rdx
  jl label_985
  jmp label_986
addToVec_conclusion:

  addq $0, %rsp
  subq $8, %r15
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
main_start:
  leaq addToVec(%rip), %rdx
  movq %rdx, %rax
  callq *%rax
  movq %rax, %rdx
  movq %rdx, %r11
  movq 8(%r11), %rdx
  movq %rdx, %r11
  movq 8(%r11), %rdx
  movq %rdx, %rax
  jmp main_conclusion
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
