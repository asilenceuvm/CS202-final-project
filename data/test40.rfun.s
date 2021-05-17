
  .globl createVec
createVec:
  pushq %rbp
  movq %rsp, %rbp
  subq $80, %rsp
  pushq %rbx
  pushq %r12
  pushq %r13
  pushq %r14

  movq $0, (%r15)
  addq $8, %r15
  movq $0, (%r15)
  addq $8, %r15
  movq $0, (%r15)
  addq $8, %r15
  movq $0, (%r15)
  addq $8, %r15
  movq $0, (%r15)
  addq $8, %r15
  movq $0, (%r15)
  addq $8, %r15
  movq $0, (%r15)
  addq $8, %r15
  movq $0, (%r15)
  addq $8, %r15

  jmp createVec_start
label_1216:
  movq free_ptr(%rip), %rdx
  addq $24, free_ptr(%rip)
  movq %rdx, %r11
  movq $5, 0(%r11)
  movq %rdx, %r11
  movq %rbx, 8(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %r12, 16(%r11)
  movq $0, %rcx
  movq %rdx, %rdx
  movq %rdx, %rax
  jmp createVec_conclusion
label_1217:
  movq $0, %rdx
  jmp label_1216
label_1218:
  movq %r15, %rdi
  movq $24, %rsi
  callq collect
  jmp label_1216
label_1219:
  movq free_ptr(%rip), %rdx
  addq $72, free_ptr(%rip)
  movq %rdx, %r11
  movq $17, 0(%r11)
  movq %rdx, %r11
  movq %r12, 8(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -88(%rbp), %rax
  movq %rax, 16(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %r14, 24(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %rbx, 32(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -32(%rbp), %rax
  movq %rax, 40(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -72(%rbp), %rax
  movq %rax, 48(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %r13, 56(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -48(%rbp), %rax
  movq %rax, 64(%r11)
  movq $0, %rcx
  movq %rdx, %rdx
  movq $42, %rbx
  movq -48(%r15), %r11
  movq 16(%r11), %rcx
  movq -64(%r15), %r11
  movq 16(%r11), %rsi
  movq -8(%r15), %r11
  movq 16(%r11), %rdi
  movq -32(%r15), %r11
  movq 16(%r11), %r8
  movq -40(%r15), %r11
  movq 16(%r11), %r9
  movq -56(%r15), %r11
  movq 16(%r11), %r10
  movq -16(%r15), %r11
  movq 16(%r11), %r12
  movq -24(%r15), %r11
  movq 16(%r11), %r13
  movq %rdx, %r11
  movq 16(%r11), %rdx
  movq %r13, %r13
  addq %rdx, %r13
  movq %r12, %rdx
  addq %r13, %rdx
  movq %r10, %r10
  addq %rdx, %r10
  movq %r9, %rdx
  addq %r10, %rdx
  movq %r8, %r8
  addq %rdx, %r8
  movq %rdi, %rdx
  addq %r8, %rdx
  movq %rsi, %rsi
  addq %rdx, %rsi
  movq %rcx, %r12
  addq %rsi, %r12
  movq free_ptr(%rip), %rdx
  movq %rdx, %rcx
  addq $24, %rcx
  movq fromspace_end(%rip), %rdx
  cmpq %rdx, %rcx
  jl label_1217
  jmp label_1218
label_1220:
  movq $0, %rdx
  jmp label_1219
label_1221:
  movq %r15, %rdi
  movq $72, %rsi
  callq collect
  jmp label_1219
label_1222:
  movq free_ptr(%rip), %rdx
  addq $72, free_ptr(%rip)
  movq %rdx, %r11
  movq $17, 0(%r11)
  movq %rdx, %r11
  movq -32(%rbp), %rax
  movq %rax, 8(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %r12, 16(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -72(%rbp), %rax
  movq %rax, 24(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %rbx, 32(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -40(%rbp), %rax
  movq %rax, 40(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -48(%rbp), %rax
  movq %rax, 48(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %r13, 56(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %r14, 64(%r11)
  movq $0, %rcx
  movq %rdx, -24(%r15)
  movq $1, %r12
  movq $2, -88(%rbp)
  movq $3, %r14
  movq $4, %rbx
  movq $5, -32(%rbp)
  movq $6, -72(%rbp)
  movq $7, %r13
  movq $8, -48(%rbp)
  movq free_ptr(%rip), %rdx
  movq %rdx, %rdx
  addq $72, %rdx
  movq fromspace_end(%rip), %rcx
  cmpq %rcx, %rdx
  jl label_1220
  jmp label_1221
label_1223:
  movq $0, %rdx
  jmp label_1222
label_1224:
  movq %r15, %rdi
  movq $72, %rsi
  callq collect
  jmp label_1222
label_1225:
  movq free_ptr(%rip), %rdx
  addq $72, free_ptr(%rip)
  movq %rdx, %r11
  movq $17, 0(%r11)
  movq %rdx, %r11
  movq %rbx, 8(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -16(%rbp), %rax
  movq %rax, 16(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %r12, 24(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %r14, 32(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %r13, 40(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -32(%rbp), %rax
  movq %rax, 48(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -40(%rbp), %rax
  movq %rax, 56(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -48(%rbp), %rax
  movq %rax, 64(%r11)
  movq $0, %rcx
  movq %rdx, -16(%r15)
  movq $1, -32(%rbp)
  movq $2, %r12
  movq $3, -72(%rbp)
  movq $4, %rbx
  movq $5, -40(%rbp)
  movq $6, -48(%rbp)
  movq $7, %r13
  movq $8, %r14
  movq free_ptr(%rip), %rdx
  movq %rdx, %rdx
  addq $72, %rdx
  movq fromspace_end(%rip), %rcx
  cmpq %rcx, %rdx
  jl label_1223
  jmp label_1224
label_1226:
  movq $0, %rdx
  jmp label_1225
label_1227:
  movq %r15, %rdi
  movq $72, %rsi
  callq collect
  jmp label_1225
label_1228:
  movq free_ptr(%rip), %rdx
  addq $72, free_ptr(%rip)
  movq %rdx, %r11
  movq $17, 0(%r11)
  movq %rdx, %r11
  movq -56(%rbp), %rax
  movq %rax, 8(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %r13, 16(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %rbx, 24(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -16(%rbp), %rax
  movq %rax, 32(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -32(%rbp), %rax
  movq %rax, 40(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -40(%rbp), %rax
  movq %rax, 48(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %r12, 56(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %r14, 64(%r11)
  movq $0, %rcx
  movq %rdx, -56(%r15)
  movq $1, %rbx
  movq $2, -16(%rbp)
  movq $3, %r12
  movq $4, %r14
  movq $5, %r13
  movq $6, -32(%rbp)
  movq $7, -40(%rbp)
  movq $8, -48(%rbp)
  movq free_ptr(%rip), %rdx
  movq %rdx, %rcx
  addq $72, %rcx
  movq fromspace_end(%rip), %rdx
  cmpq %rdx, %rcx
  jl label_1226
  jmp label_1227
label_1229:
  movq $0, %rdx
  jmp label_1228
label_1230:
  movq %r15, %rdi
  movq $72, %rsi
  callq collect
  jmp label_1228
label_1231:
  movq free_ptr(%rip), %rdx
  addq $72, free_ptr(%rip)
  movq %rdx, %r11
  movq $17, 0(%r11)
  movq %rdx, %r11
  movq %r13, 8(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -16(%rbp), %rax
  movq %rax, 16(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -56(%rbp), %rax
  movq %rax, 24(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %r14, 32(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -40(%rbp), %rax
  movq %rax, 40(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -80(%rbp), %rax
  movq %rax, 48(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %r12, 56(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %rbx, 64(%r11)
  movq $0, %rcx
  movq %rdx, -40(%r15)
  movq $1, -56(%rbp)
  movq $2, %r13
  movq $3, %rbx
  movq $4, -16(%rbp)
  movq $5, -32(%rbp)
  movq $6, -40(%rbp)
  movq $7, %r12
  movq $8, %r14
  movq free_ptr(%rip), %rdx
  movq %rdx, %rdx
  addq $72, %rdx
  movq fromspace_end(%rip), %rcx
  cmpq %rcx, %rdx
  jl label_1229
  jmp label_1230
label_1232:
  movq $0, %rdx
  jmp label_1231
label_1233:
  movq %r15, %rdi
  movq $72, %rsi
  callq collect
  jmp label_1231
label_1234:
  movq free_ptr(%rip), %rdx
  addq $72, free_ptr(%rip)
  movq %rdx, %r11
  movq $17, 0(%r11)
  movq %rdx, %r11
  movq -64(%rbp), %rax
  movq %rax, 8(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -80(%rbp), %rax
  movq %rax, 16(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %r14, 24(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -16(%rbp), %rax
  movq %rax, 32(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -40(%rbp), %rax
  movq %rax, 40(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %r12, 48(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %r13, 56(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %rbx, 64(%r11)
  movq $0, %rcx
  movq %rdx, -32(%r15)
  movq $1, %r13
  movq $2, -16(%rbp)
  movq $3, -56(%rbp)
  movq $4, %r14
  movq $5, -40(%rbp)
  movq $6, -80(%rbp)
  movq $7, %r12
  movq $8, %rbx
  movq free_ptr(%rip), %rdx
  movq %rdx, %rcx
  addq $72, %rcx
  movq fromspace_end(%rip), %rdx
  cmpq %rdx, %rcx
  jl label_1232
  jmp label_1233
label_1235:
  movq $0, %rdx
  jmp label_1234
label_1236:
  movq %r15, %rdi
  movq $72, %rsi
  callq collect
  jmp label_1234
label_1237:
  movq free_ptr(%rip), %rdx
  addq $72, free_ptr(%rip)
  movq %rdx, %r11
  movq $17, 0(%r11)
  movq %rdx, %r11
  movq -24(%rbp), %rax
  movq %rax, 8(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %r13, 16(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -40(%rbp), %rax
  movq %rax, 24(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %r12, 32(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -64(%rbp), %rax
  movq %rax, 40(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %rbx, 48(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %r14, 56(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -16(%rbp), %rax
  movq %rax, 64(%r11)
  movq $0, %rcx
  movq %rdx, -8(%r15)
  movq $1, -64(%rbp)
  movq $2, -80(%rbp)
  movq $3, %r14
  movq $4, -16(%rbp)
  movq $5, -40(%rbp)
  movq $6, %r12
  movq $7, %r13
  movq $8, %rbx
  movq free_ptr(%rip), %rdx
  movq %rdx, %rcx
  addq $72, %rcx
  movq fromspace_end(%rip), %rdx
  cmpq %rdx, %rcx
  jl label_1235
  jmp label_1236
label_1238:
  movq $0, %rdx
  jmp label_1237
label_1239:
  movq %r15, %rdi
  movq $72, %rsi
  callq collect
  jmp label_1237
label_1240:
  movq free_ptr(%rip), %rdx
  addq $72, free_ptr(%rip)
  movq %rdx, %r11
  movq $17, 0(%r11)
  movq %rdx, %r11
  movq -64(%rbp), %rax
  movq %rax, 8(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %r14, 16(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -40(%rbp), %rax
  movq %rax, 24(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %r12, 32(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %rbx, 40(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -16(%rbp), %rax
  movq %rax, 48(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -24(%rbp), %rax
  movq %rax, 56(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %r13, 64(%r11)
  movq $0, %rcx
  movq %rdx, -64(%r15)
  movq $1, -24(%rbp)
  movq $2, %r13
  movq $3, -40(%rbp)
  movq $4, %r12
  movq $5, -64(%rbp)
  movq $6, %rbx
  movq $7, %r14
  movq $8, -16(%rbp)
  movq free_ptr(%rip), %rdx
  movq %rdx, %rcx
  addq $72, %rcx
  movq fromspace_end(%rip), %rdx
  cmpq %rdx, %rcx
  jl label_1238
  jmp label_1239
label_1241:
  movq $0, %rdx
  jmp label_1240
label_1242:
  movq %r15, %rdi
  movq $72, %rsi
  callq collect
  jmp label_1240
label_1243:
  movq free_ptr(%rip), %rdx
  addq $72, free_ptr(%rip)
  movq %rdx, %r11
  movq $17, 0(%r11)
  movq %rdx, %r11
  movq %r12, 8(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %r13, 16(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -16(%rbp), %rax
  movq %rax, 24(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -64(%rbp), %rax
  movq %rax, 32(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %rbx, 40(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -40(%rbp), %rax
  movq %rax, 48(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %r14, 56(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq -24(%rbp), %rax
  movq %rax, 64(%r11)
  movq $0, %rcx
  movq %rdx, -48(%r15)
  movq $1, -64(%rbp)
  movq $2, %r14
  movq $3, -40(%rbp)
  movq $4, %r12
  movq $5, %rbx
  movq $6, -16(%rbp)
  movq $7, -24(%rbp)
  movq $8, %r13
  movq free_ptr(%rip), %rdx
  movq %rdx, %rdx
  addq $72, %rdx
  movq fromspace_end(%rip), %rcx
  cmpq %rcx, %rdx
  jl label_1241
  jmp label_1242
label_1244:
  movq $0, %rdx
  jmp label_1243
label_1245:
  movq %r15, %rdi
  movq $72, %rsi
  callq collect
  jmp label_1243
createVec_start:
  movq $1, %r12
  movq $2, %r13
  movq $3, -16(%rbp)
  movq $4, -64(%rbp)
  movq $5, %rbx
  movq $6, -40(%rbp)
  movq $7, %r14
  movq $8, -24(%rbp)
  movq free_ptr(%rip), %rdx
  movq %rdx, %rcx
  addq $72, %rcx
  movq fromspace_end(%rip), %rdx
  cmpq %rdx, %rcx
  jl label_1244
  jmp label_1245
createVec_conclusion:

  addq $80, %rsp
  subq $64, %r15
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
  leaq createVec(%rip), %rdx
  movq %rdx, %rax
  callq *%rax
  movq %rax, %rdx
  movq %rdx, %r11
  movq 16(%r11), %rdx
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
