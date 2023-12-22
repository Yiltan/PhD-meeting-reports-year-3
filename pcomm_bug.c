#include <mpi.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

#define MPI_CHECK(cmd)                                                      \
{                                                                           \
    int _error = cmd;                                                       \
    if(_error != MPI_SUCCESS)                                               \
    {                                                                       \
        int _rank;                                                          \
        MPI_Comm_rank(MPI_COMM_WORLD, &_rank);                              \
        printf("[%d] <%s>:%i error=%d", _rank, __FILE__, __LINE__, _error); \
        MPI_Abort(MPI_COMM_WORLD, _error);                                  \
    }                                                                       \
}

int main()
{
    // Initialize the MPI environment
    int provided;
    MPI_Init_thread(NULL, NULL, MPI_THREAD_MULTIPLE, &provided);

    if (MPI_THREAD_MULTIPLE != provided)
    {
        MPI_Abort(MPI_COMM_WORLD, -1);
    }

    int rank;
    MPI_CHECK(MPI_Comm_rank(MPI_COMM_WORLD, &rank));

    int partitions = 16;
    int count = 1024;
    int *buffer = calloc(partitions * count, sizeof(int));

    MPI_Request sreq;
    MPI_Request rreq;

    // Init
    if (0 == rank)
    {
        MPI_CHECK(MPI_Psend_init(buffer, partitions, count,
                                 MPI_INT, 1, 123, MPI_COMM_WORLD,
                                 MPI_INFO_NULL, &sreq));
    }
    else if (1 == rank)
    {
        MPI_CHECK(MPI_Precv_init(buffer, partitions, count,
                                 MPI_INT, 0, 123, MPI_COMM_WORLD,
                                 MPI_INFO_NULL, &rreq));

        MPI_CHECK(MPI_Psend_init(buffer, partitions, count,
                                 MPI_INT, 2, 123, MPI_COMM_WORLD,
                                 MPI_INFO_NULL, &sreq));
    }
    else if (2 == rank)
    {
        MPI_CHECK(MPI_Precv_init(buffer, partitions, count,
                                 MPI_INT, 1, 123, MPI_COMM_WORLD,
                                 MPI_INFO_NULL, &rreq));
    }

    // Main Loop
    for (int i=0; i<2; i++)
    {
        if (0 == rank)
        {
            MPI_CHECK(MPI_Start(&sreq));

            #pragma omp parallel for shared(sreq)
            for (int p=0; p<partitions; p++)
            {
                MPI_CHECK(MPI_Pready(p, sreq));
            }

            MPI_CHECK(MPI_Wait(&sreq, MPI_STATUS_IGNORE));
            printf("Done Rank 0\n");
            fflush(stdout);
        }
        else if (1 == rank)
        {
            MPI_CHECK(MPI_Start(&rreq));
            MPI_CHECK(MPI_Start(&sreq));

            #pragma omp parallel for shared(sreq, rreq)
            for (int p=0; p<partitions; p++)
            {
                volatile int flag = 0;
                do {
                    MPI_CHECK(MPI_Parrived(rreq, p, (int*) &flag));
                } while (1 != flag);

                MPI_CHECK(MPI_Pready(p, sreq));
            }

            MPI_CHECK(MPI_Wait(&rreq, MPI_STATUS_IGNORE));
            printf("Done Rank R1\n");
            fflush(stdout);

            MPI_CHECK(MPI_Wait(&sreq, MPI_STATUS_IGNORE));
            printf("Done Rank S1\n");
            fflush(stdout);
        }
        else if (2 == rank)
        {
            MPI_CHECK(MPI_Start(&rreq));

            #pragma omp parallel for shared(rreq)
            for (int p=0; p<partitions; p++)
            {
                volatile int flag = 0;
                do {
                    MPI_CHECK(MPI_Parrived(rreq, p, (int*) &flag));
                } while (1 != flag);
            }

            MPI_CHECK(MPI_Wait(&rreq, MPI_STATUS_IGNORE));
            printf("Done Rank 2\n");
            fflush(stdout);
        }
    }

    // Free Requests
    if (0 == rank)
    {
        MPI_CHECK(MPI_Request_free(&sreq));
    }
    else if (1 == rank)
    {
        MPI_CHECK(MPI_Request_free(&sreq));
        MPI_CHECK(MPI_Request_free(&rreq));
    }
    else if (2 == rank)
    {
        MPI_CHECK(MPI_Request_free(&rreq));
    }

    MPI_Finalize();
    return 0;
}

